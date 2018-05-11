from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _RawText as RawText
from Entity import _RawTextType as RawTextType
from Entity import _RawTextPair as RawTextPair
from Entity import _Detection as Detection
from Entity.PreProcessing import _RawTextExcerptLocation as RawTextExcerptLocation
from Entity import _EnumYesNo as EnumYesNo
from Entity import _PlagiarismObfuscation as PlagiarismObfuscation
from Entity import _PlagiarismType as PlagiarismType
from Entity import _PanDetectionXmlPlain as PanDetectionXmlPlain
from Entity import _PanFolderStructure as PanFolderStructure
from Repository import _TextCollectionMetaRepository as TextCollectionMetaRepository
from Repository import _RawTextRepository as RawTextRepository
from Repository import _RawTextPairRepository as RawTextPairRepository
from Repository import _RawTextExcerptLocationRepository as RawTextExcerptLocationRepository
from Repository import _DetectionRepository as DetectionRepository
from Repository import _PanRepository as PanRepository
from Process import _BaseProcess as BaseProcess
import os
import random
from distutils.dir_util import copy_tree
from datetime import datetime

class DataImportationProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from DataImportationProcess')
        print ('Hello, I\'m the DataImportationProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')

    def ImportFromPanFiles(self, textCollectionMeta, folderCompletePath):
        textCollectionMetaId = self.SaveTextCollection(textCollectionMeta = textCollectionMeta)
        rawTextList = self.GetRawTexts(
            folderCompletePath = folderCompletePath, 
            textCollectionMetaId = textCollectionMetaId)
        self.SaveRawTextList(rawTextList = rawTextList)
        rawTextPairList = self.GetRawTextPairList(
            folderCompletePath = folderCompletePath, 
            textCollectionMetaId = textCollectionMetaId)
        self.SaveRawTextPairList(rawTextPairList = rawTextPairList)
        detectionList= self.ExtractDetectionList(
            folderCompletePath = folderCompletePath,
            textCollectionMetaId = textCollectionMetaId)
        self.SaveDetectionList(detectionList = detectionList)

    def SaveTextCollection(self, textCollectionMeta):
        self._textCollectionMetaRepository.Insert(textCollectionMeta)
        return textCollectionMeta.id

    def GetRawTexts(self, folderCompletePath, textCollectionMetaId):
        suspiciousFilesFolderPath = os.path.join(folderCompletePath, PanFolderStructure.SUSPICIOUS_RAW_TEXT_FOLDER)
        suspiciousRawTextList = self._panRepository.GetRawTextListFromDirectoryOfTexts(
            filesFolderPath = suspiciousFilesFolderPath,
            rawTextType = RawTextType.suspicious,
            textCollectionMetaId = textCollectionMetaId)
        sourceFilesFolderPath = os.path.join(folderCompletePath, PanFolderStructure.SOURCE_RAW_TEXTS_FOLDER)
        sourceRawTextList = self._panRepository.GetRawTextListFromDirectoryOfTexts(
            filesFolderPath = sourceFilesFolderPath,
            rawTextType = RawTextType.source,
            textCollectionMetaId = textCollectionMetaId)
        rawTextList = suspiciousRawTextList + sourceRawTextList
        return rawTextList
        
    def SaveRawTextList(self, rawTextList):
        self._rawTextRepository.InsertList(rawTextList)

    def GetRawTextPairList(self, folderCompletePath, textCollectionMetaId):
        pairsFilePath = os.path.join(folderCompletePath, PanFolderStructure.PAIRS_FILE_NAME)
        tupleFileNameSuspiciousSourceList = self._panRepository.GetTupleFileNameSuspiciousSourceList(
            pairsFilePath = pairsFilePath)
        rawTextPairList = []
        for tupleFileNameSuspiciousSource in tupleFileNameSuspiciousSourceList:
            tupleRawTextIdsSuspiciousSource = self._rawTextRepository.GetTupleRawTextIdsSuspiciousSource(
                tupleFileNameSuspiciousSource = tupleFileNameSuspiciousSource,
                textCollectionMetaId = textCollectionMetaId)
            if(tupleRawTextIdsSuspiciousSource is None):
                continue
            rawTextPair = RawTextPair(
                suspiciousRawTextId = tupleRawTextIdsSuspiciousSource[0], 
                sourceRawTextId = tupleRawTextIdsSuspiciousSource[1])
            rawTextPairList.append(rawTextPair)
        return rawTextPairList
    
    def SaveRawTextPairList(self, rawTextPairList):
        self._rawTextPairRepository.InsertList(rawTextPairList)        

    def GetPanDetectionXmlPlainList(self, folderCompletePath):
        detectionFolderPathList = self.GetExistingDetectionFolders(folderCompletePath)
        panDetectionXmlPlainList = []
        for detectionFolderPath in detectionFolderPathList:
            panDetectionXmlPlainList = panDetectionXmlPlainList + self._panRepository.GetPanDetectionXmlPlainListFromDiretory(
                filesFolderPath = detectionFolderPath)
        return panDetectionXmlPlainList

    def GetExistingDetectionFolders(self, folderCompletePath):
        detectionFolderPathList = [
            os.path.join(folderCompletePath, detectionFolderName) for detectionFolderName in PanFolderStructure.DETECTION_FOLDER_NAME_LIST]
        detectionFolderPathList = list(filter(lambda folderPath: os.path.isdir(folderPath), detectionFolderPathList))
        return detectionFolderPathList

    def ExtractRawTextExcerptLocationDistinctList(self, panDetectionXmlPlainList, textCollectionMetaId):
        rawTextExcerptLocationList = []
        for panDetectionXmlPlain in panDetectionXmlPlainList:
            tupleRawTextIdsSuspiciousSource = self._rawTextRepository.GetTupleRawTextIdsSuspiciousSource(
                tupleFileNameSuspiciousSource = (panDetectionXmlPlain.suspiciousFileName, panDetectionXmlPlain.sourceFileName), 
                textCollectionMetaId = textCollectionMetaId)
            suspiciousRawTextExcerptLocation = RawTextExcerptLocation(
                stringLength = panDetectionXmlPlain.suspiciousLength,
                firstCharacterPosition = panDetectionXmlPlain.suspiciousOffset,
                preProcessedDataId = None,
                rawTextId = tupleRawTextIdsSuspiciousSource[0])
            sourceRawTextExcerptLocation = RawTextExcerptLocation(
                stringLength = panDetectionXmlPlain.sourceLength,
                firstCharacterPosition = panDetectionXmlPlain.sourceOffset,
                preProcessedDataId = None,
                rawTextId = tupleRawTextIdsSuspiciousSource[1])
            rawTextExcerptLocationList.append(suspiciousRawTextExcerptLocation)
            rawTextExcerptLocationList.append(sourceRawTextExcerptLocation)
        rawTextExcerptLocationDistinctList = list(set(rawTextExcerptLocationList))
        return rawTextExcerptLocationDistinctList

    def FillIdsRawTextExcerptLocationList(self, rawTextExcerptLocationList):
        self._rawTextExcerptLocationRepository.InsertList(rawTextExcerptLocationList)
        return rawTextExcerptLocationList

    def GetDetectionList(self, panDetectionXmlPlainList, rawTextExcerptLocationList,
        textCollectionMetaId):
        detectionList = []
        for panDetectionXmlPlain in panDetectionXmlPlainList:
            tupleRawTextIdsSuspiciousSource = self._rawTextRepository.GetTupleRawTextIdsSuspiciousSource(
                tupleFileNameSuspiciousSource = (panDetectionXmlPlain.suspiciousFileName, panDetectionXmlPlain.sourceFileName), 
                textCollectionMetaId = textCollectionMetaId)
            _rawTextSuspiciousLocationId = next(
                item.id for item in rawTextExcerptLocationList if (
                    item.rawTextId == tupleRawTextIdsSuspiciousSource[0] and
                    item.firstCharacterPosition == panDetectionXmlPlain.suspiciousOffset and
                    item.stringLength == panDetectionXmlPlain.suspiciousLength))
            _rawTextSourceLocationId = next(
                item.id for item in rawTextExcerptLocationList if (
                    item.rawTextId == tupleRawTextIdsSuspiciousSource[1] and
                    item.firstCharacterPosition == panDetectionXmlPlain.sourceOffset and
                    item.stringLength == panDetectionXmlPlain.sourceLength))
            detection = Detection(
                textCollectionMetaId = textCollectionMetaId,
                rawTextSuspiciousLocationId = _rawTextSuspiciousLocationId, 
                rawTextSourceLocationId = _rawTextSourceLocationId,
                _type = PlagiarismType.FromString(panDetectionXmlPlain._type),
                obfuscationDegree = panDetectionXmlPlain.obfuscationDegree,
                obfuscation = PlagiarismObfuscation.FromString(panDetectionXmlPlain.obfuscation),
                name = panDetectionXmlPlain.name,
                isGiven = EnumYesNo.yes,
                isDetected = EnumYesNo.no)
            detectionList.append(detection)
        return detectionList

    def ExtractDetectionList(self, folderCompletePath, textCollectionMetaId):
        panDetectionXmlPlainList = self.GetPanDetectionXmlPlainList(folderCompletePath = folderCompletePath)
        rawTextExcerptLocationList = self.ExtractRawTextExcerptLocationDistinctList(
            panDetectionXmlPlainList = panDetectionXmlPlainList, 
            textCollectionMetaId = textCollectionMetaId)
        rawTextExcerptLocationList = self.FillIdsRawTextExcerptLocationList(
            rawTextExcerptLocationList = rawTextExcerptLocationList)
        detectionList = self.GetDetectionList(
            panDetectionXmlPlainList = panDetectionXmlPlainList, 
            rawTextExcerptLocationList = rawTextExcerptLocationList,
            textCollectionMetaId = textCollectionMetaId)
        return detectionList

    def SaveDetectionList(self, detectionList):
        self._detectionRepository.InsertList(detectionList) 

    def DecreasePanDataBaseInNewFolder(self, decreasePercentage, folderCompletePath):
        remainingPercentage = 1 - decreasePercentage
        newFolderCompletePath = DataImportationProcess.CreateNewDirectoryDecreasedDataBase(
            folderCompletePath, remainingPercentage)
        
        pairsOfRawTextsFilePath = os.path.join(newFolderCompletePath, PanFolderStructure.PAIRS_FILE_NAME)
        tupleFileNameSuspiciousSourceList = self._panRepository.GetTupleFileNameSuspiciousSourceList(
            pairsFilePath = pairsOfRawTextsFilePath)
        numberOfTuplesKeeping = int(len(tupleFileNameSuspiciousSourceList) * remainingPercentage)
        keptTupleFileNameSuspiciousSourceList = DataImportationProcess.GetRandomSubset(
            iterator = tupleFileNameSuspiciousSourceList, K = numberOfTuplesKeeping)
        
        notKeepTupleFileNameSuspiciousSourceList = DataImportationProcess.GetTupleFileNameSuspiciousSourceListToRemove(
            keptTupleFileNameSuspiciousSourceList, tupleFileNameSuspiciousSourceList)
        DataImportationProcess.RemoveSuspiciousRawTextsByTupleFileList(
            notKeepTupleFileNameSuspiciousSourceList, newFolderCompletePath)
        DataImportationProcess.RemoveSourceRawTextsByTupleFileList(
            notKeepTupleFileNameSuspiciousSourceList, newFolderCompletePath)

        self.UpdatePairFile(
                folderPath = newFolderCompletePath,
                keptTupleFileNameSuspiciousSourceList = keptTupleFileNameSuspiciousSourceList)

        self.DecreaseDetectionFolders(
            newFolderCompletePath, keptTupleFileNameSuspiciousSourceList)
        
        return newFolderCompletePath
    
    def CreateNewDirectoryDecreasedDataBase(folderCompletePath, percentage):
        dateTimeString = datetime.now().strftime('%Y%m%d_%H%M%S')
        newFolderCompletePath =\
            os.path.dirname(folderCompletePath) +\
            '_' + dateTimeString +\
            '_p' +\
            "{:.0f}".format(100 * percentage)
        if(not os.path.exists(newFolderCompletePath)):
            os.makedirs(newFolderCompletePath)
        DataImportationProcess.CopyEntireFolder(
            folder = folderCompletePath, 
            newFolderPath = newFolderCompletePath)
        return newFolderCompletePath

    def CopyEntireFolder(folder, newFolderPath):
        # External source code from here: https://stackoverflow.com/questions/15034151/copy-directory-contents-into-a-directory-with-python
        copy_tree(src = folder, dst = newFolderPath, 
            preserve_mode = True, preserve_times = True, preserve_symlinks = True)

    @staticmethod
    def GetRandomSubset(iterator, K ):
        # External source code from here: https://stackoverflow.com/questions/2612648/reservoir-sampling
        result = []
        N = 0
        for item in iterator:
            N += 1
            if len( result ) < K:
                result.append( item )
            else:
                s = int(random.random() * N)
                if s < K:
                    result[ s ] = item
        return result

    def GetTupleFileNameSuspiciousSourceListToRemove(keptTupleFileNameSuspiciousSourceList, tupleFileNameSuspiciousSourceList):
        notKeepTupleFileNameSuspiciousSourceList = list(
            filter(
                lambda _tuple: _tuple not in keptTupleFileNameSuspiciousSourceList, 
                tupleFileNameSuspiciousSourceList))
        return notKeepTupleFileNameSuspiciousSourceList

    def RemoveFilesList(filePathList):
        for filePath in filePathList:
            os.remove(filePath)
        
    def RemoveSuspiciousRawTextsByTupleFileList(notKeepTupleFileNameSuspiciousSourceList, folderCompletePath):
        removeListWithDuplicates = list(map(
            lambda tupleFileNameSuspiciousSource: os.path.join(
                folderCompletePath, 
                PanFolderStructure.SUSPICIOUS_RAW_TEXT_FOLDER,
                tupleFileNameSuspiciousSource[0]),
            notKeepTupleFileNameSuspiciousSourceList))
        removeList = list(set(removeListWithDuplicates))
        DataImportationProcess.RemoveFilesList(filePathList = removeList)
    
    def RemoveSourceRawTextsByTupleFileList(notKeepTupleFileNameSuspiciousSourceList, folderCompletePath):
        removeListWithDuplicates = list(map(
            lambda tupleFileNameSuspiciousSource: os.path.join(
                folderCompletePath, 
                PanFolderStructure.SOURCE_RAW_TEXTS_FOLDER,
                tupleFileNameSuspiciousSource[1]),
            notKeepTupleFileNameSuspiciousSourceList))
        removeList = list(set(removeListWithDuplicates))
        DataImportationProcess.RemoveFilesList(filePathList = removeList)

    def UpdatePairFile(self, folderPath, keptTupleFileNameSuspiciousSourceList):
        pairsLines = []
        for keptTupleFileNameSuspiciousSource in keptTupleFileNameSuspiciousSourceList:
            pairsLines.append(
                keptTupleFileNameSuspiciousSource[0] + ' ' + keptTupleFileNameSuspiciousSource[1])
        pairsFilePath = os.path.join(folderPath, PanFolderStructure.PAIRS_FILE_NAME)
        self._panRepository.UpdatePairsFile(
            pairsFilePath = pairsFilePath, pairsLines = pairsLines)

    def DecreaseDetectionFolders(self, folderCompletePath, keptTupleFileNameSuspiciousSourceList):
        detectionFolderPathList = self.GetExistingDetectionFolders(folderCompletePath)
        for detectionFolderPath in detectionFolderPathList:
            tupleFileNameSuspiciousSourceDetectionList = self.GetTupleFileNameSuspiciousSourceDetectionList(detectionFolderPath)
            keptTupleFileNameSuspiciousSourceDetectionList = list(
                filter(
                    lambda _tuple: _tuple in keptTupleFileNameSuspiciousSourceList, 
                    tupleFileNameSuspiciousSourceDetectionList))
            notKeepTupleFileNameSuspiciousSourceList = DataImportationProcess.GetTupleFileNameSuspiciousSourceListToRemove(
                keptTupleFileNameSuspiciousSourceDetectionList, tupleFileNameSuspiciousSourceDetectionList)
            detectionFileNameListToRemove = DataImportationProcess.GetDetectionFileNameListFromTupleFile(
                tupleFileNameSuspiciousSourceDetectionList = notKeepTupleFileNameSuspiciousSourceList)
            DataImportationProcess.RemoveDetectionsAtTheList(
                detectionFolderPath = detectionFolderPath, 
                detectionFileNameList = detectionFileNameListToRemove)
            self.UpdatePairFile(
                folderPath = detectionFolderPath,
                keptTupleFileNameSuspiciousSourceList = keptTupleFileNameSuspiciousSourceDetectionList)
    
    def GetTupleFileNameSuspiciousSourceDetectionList(self, detectionFolderPath):
        detectionPairFilePath =  os.path.join(detectionFolderPath, PanFolderStructure.PAIRS_FILE_NAME)
        tupleFileNameSuspiciousSourceDetectionList = self._panRepository.GetTupleFileNameSuspiciousSourceList(
            pairsFilePath = detectionPairFilePath)
        return tupleFileNameSuspiciousSourceDetectionList
    
    def GetDetectionFileNameListFromTupleFile(tupleFileNameSuspiciousSourceDetectionList):
        detectionFileNameList = []
        for tupleFileNameSuspiciousSourceDetection in tupleFileNameSuspiciousSourceDetectionList:
            detectionFileName =\
                tupleFileNameSuspiciousSourceDetection[0].split('.txt')[0] +\
                '-' +\
                tupleFileNameSuspiciousSourceDetection[1].split('.txt')[0] +\
                '.xml'
            detectionFileNameList.append(detectionFileName)
        return detectionFileNameList

    def RemoveDetectionsAtTheList(detectionFolderPath, detectionFileNameList):
        detectionFilePathList = [
            os.path.join(detectionFolderPath,detectionFileName)
            for detectionFileName in detectionFileNameList]
        DataImportationProcess.RemoveFilesList(
            filePathList = detectionFilePathList)


    _textCollectionMetaRepository = TextCollectionMetaRepository()
    _rawTextRepository = RawTextRepository()
    _rawTextPairRepository = RawTextPairRepository()
    _rawTextExcerptLocationRepository = RawTextExcerptLocationRepository()
    _detectionRepository = DetectionRepository()
    _panRepository = PanRepository()

    def __init__(self):
        super().__init__()
