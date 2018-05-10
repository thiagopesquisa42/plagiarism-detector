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
        detectionFolderPathList = [
            os.path.join(folderCompletePath, detectionFolderName) for detectionFolderName in PanFolderStructure.DETECTION_FOLDER_NAME_LIST]
        detectionFolderPathList = list(filter(lambda folderPath: os.path.isdir(folderPath), detectionFolderPathList))
        panDetectionXmlPlainList = []
        for detectionFolderPath in detectionFolderPathList:
            panDetectionXmlPlainList = panDetectionXmlPlainList + self._panRepository.GetPanDetectionXmlPlainListFromDiretory(
                filesFolderPath = detectionFolderPath)
        return panDetectionXmlPlainList

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

    _textCollectionMetaRepository = TextCollectionMetaRepository()
    _rawTextRepository = RawTextRepository()
    _rawTextPairRepository = RawTextPairRepository()
    _rawTextExcerptLocationRepository = RawTextExcerptLocationRepository()
    _detectionRepository = DetectionRepository()
    _panRepository = PanRepository()

    def __init__(self):
        super().__init__()
