from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _RawText as RawText
from Entity import _RawTextType as RawTextType
from Entity import _RawTextPair as RawTextPair
from Entity import _Detection as Detection
from Entity import _RawTextExcerptLocation as RawTextExcerptLocation
from Entity import _EnumYesNo as EnumYesNo
from Entity import _PlagiarismObfuscation as PlagiarismObfuscation
from Entity import _PlagiarismType as PlagiarismType
from Entity import _DetectionPanXmlPlain as DetectionPanXmlPlain
from Repository import _TextCollectionMetaRepository as TextCollectionMetaRepository
from Repository import _RawTextRepository as RawTextRepository
from Repository import _RawTextPairRepository as RawTextPairRepository
from Repository import _RawTextExcerptLocationRepository as RawTextExcerptLocationRepository
from Repository import _DetectionRepository as DetectionRepository
from Repository import _PanRepository as PanRepository
from Constant import _Pan as PanConstant
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
        return self._textCollectionMetaRepository.Insert(textCollectionMeta = textCollectionMeta)

    def GetRawTexts(self, folderCompletePath, textCollectionMetaId):
        suspiciousFilesFolderPath = os.path.join(folderCompletePath, PanConstant.SUSPICIOUS_RAW_TEXT_FOLDER)
        suspiciousRawTextList = self._panRepository.GetRawTextListFromDirectoryOfTexts(
            filesFolderPath = suspiciousFilesFolderPath,
            rawTextType = RawTextType.suspicious,
            textCollectionMetaId = textCollectionMetaId)
        sourceFilesFolderPath = os.path.join(folderCompletePath, PanConstant.SOURCE_RAW_TEXTS_FOLDER)
        sourceRawTextList = self._panRepository.GetRawTextListFromDirectoryOfTexts(
            filesFolderPath = sourceFilesFolderPath,
            rawTextType = RawTextType.source,
            textCollectionMetaId = textCollectionMetaId)
        rawTextList = suspiciousRawTextList + sourceRawTextList
        return rawTextList
        
    def SaveRawTextList(self, rawTextList):
        self._rawTextRepository.InsertList(rawTextList = rawTextList)

    def GetRawTextPairList(self, folderCompletePath, textCollectionMetaId):
        pairsFilePath = os.path.join(folderCompletePath, PanConstant.PAIRS_FILE_NAME)
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
        self._rawTextPairRepository.InsertList(rawTextPairList = rawTextPairList)        

    def GetDetectionPanXmlPlainList(self, folderCompletePath):
        detectionFolderPathList = [
            os.path.join(folderCompletePath, PanConstant.NO_OBFUSCATION_DETECTION_FOLDER),
            os.path.join(folderCompletePath, PanConstant.RANDOM_OBFUSCATION_DETECTION_FOLDER)]
        detectionFolderPathList = list(filter(lambda folderPath: os.path.isdir(folderPath), detectionFolderPathList))
        detectionPanXmlPlainList = []
        for detectionFolderPath in detectionFolderPathList:
            detectionPanXmlPlainList = detectionPanXmlPlainList + self._panRepository.GetDetectionPanXmlPlainListFromDiretory(
                filesFolderPath = detectionFolderPath)
        return detectionPanXmlPlainList

    def ExtractRawTextExcerptLocationDistinctList(self, detectionPanXmlPlainList, textCollectionMetaId):
        rawTextExcerptLocationList = []
        for detectionPanXmlPlain in detectionPanXmlPlainList:
            tupleRawTextIdsSuspiciousSource = self._rawTextRepository.GetTupleRawTextIdsSuspiciousSource(
                tupleFileNameSuspiciousSource = (detectionPanXmlPlain.suspiciousFileName, detectionPanXmlPlain.sourceFileName), 
                textCollectionMetaId = textCollectionMetaId)
            suspiciousRawTextExcerptLocation = RawTextExcerptLocation(
                stringLength = detectionPanXmlPlain.suspiciousLength,
                firstCharacterPosition = detectionPanXmlPlain.suspiciousOffset,
                preProcessedDataId = None,
                rawTextId = tupleRawTextIdsSuspiciousSource[0])
            sourceRawTextExcerptLocation = RawTextExcerptLocation(
                stringLength = detectionPanXmlPlain.sourceLength,
                firstCharacterPosition = detectionPanXmlPlain.sourceOffset,
                preProcessedDataId = None,
                rawTextId = tupleRawTextIdsSuspiciousSource[1])
            rawTextExcerptLocationList.append(suspiciousRawTextExcerptLocation)
            rawTextExcerptLocationList.append(sourceRawTextExcerptLocation)
        rawTextExcerptLocationDistinctList = list(set(rawTextExcerptLocationList))
        return rawTextExcerptLocationDistinctList

    def FillIdsRawTextExcerptLocationList(self, rawTextExcerptLocationList):
        self._rawTextExcerptLocationRepository.InsertList(
            rawTextExcerptLocationList = rawTextExcerptLocationList)
        return rawTextExcerptLocationList

    def GetDetectionList(self, detectionPanXmlPlainList, rawTextExcerptLocationList,
        textCollectionMetaId):
        detectionList = []
        for detectionPanXmlPlain in detectionPanXmlPlainList:
            tupleRawTextIdsSuspiciousSource = self._rawTextRepository.GetTupleRawTextIdsSuspiciousSource(
                tupleFileNameSuspiciousSource = (detectionPanXmlPlain.suspiciousFileName, detectionPanXmlPlain.sourceFileName), 
                textCollectionMetaId = textCollectionMetaId)
            _rawTextSuspiciousLocationId = next(
                item.id for item in rawTextExcerptLocationList if (
                    item.rawTextId == tupleRawTextIdsSuspiciousSource[0] and
                    item.firstCharacterPosition == detectionPanXmlPlain.suspiciousOffset and
                    item.stringLength == detectionPanXmlPlain.suspiciousLength))
            _rawTextSourceLocationId = next(
                item.id for item in rawTextExcerptLocationList if (
                    item.rawTextId == tupleRawTextIdsSuspiciousSource[1] and
                    item.firstCharacterPosition == detectionPanXmlPlain.sourceOffset and
                    item.stringLength == detectionPanXmlPlain.sourceLength))
            detection = Detection(
                textCollectionMetaId = textCollectionMetaId,
                rawTextSuspiciousLocationId = _rawTextSuspiciousLocationId, 
                rawTextSourceLocationId = _rawTextSourceLocationId,
                _type = PlagiarismType.FromString(detectionPanXmlPlain._type),
                obfuscationDegree = detectionPanXmlPlain.obfuscationDegree,
                obfuscation = PlagiarismObfuscation.FromString(detectionPanXmlPlain.obfuscation),
                name = detectionPanXmlPlain.name,
                isGiven = EnumYesNo.yes,
                isDetected = EnumYesNo.no)
            detectionList.append(detection)
        return detectionList

    def ExtractDetectionList(self, folderCompletePath, textCollectionMetaId):
        detectionPanXmlPlainList = self.GetDetectionPanXmlPlainList(folderCompletePath = folderCompletePath)
        rawTextExcerptLocationList = self.ExtractRawTextExcerptLocationDistinctList(
            detectionPanXmlPlainList = detectionPanXmlPlainList, 
            textCollectionMetaId = textCollectionMetaId)
        rawTextExcerptLocationList = self.FillIdsRawTextExcerptLocationList(
            rawTextExcerptLocationList = rawTextExcerptLocationList)
        detectionList = self.GetDetectionList(
            detectionPanXmlPlainList = detectionPanXmlPlainList, 
            rawTextExcerptLocationList = rawTextExcerptLocationList,
            textCollectionMetaId = textCollectionMetaId)
        return detectionList

    def SaveDetectionList(self, detectionList):
        self._detectionRepository.InsertList(detectionList = detectionList) 

    _textCollectionMetaRepository = TextCollectionMetaRepository()
    _rawTextRepository = RawTextRepository()
    _rawTextPairRepository = RawTextPairRepository()
    _rawTextExcerptLocationRepository = RawTextExcerptLocationRepository()
    _detectionRepository = DetectionRepository()
    _panRepository = PanRepository()

    def __init__(self):
        super().__init__()
