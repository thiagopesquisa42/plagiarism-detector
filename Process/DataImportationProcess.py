from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _RawText as RawText
from Entity import _RawTextType as RawTextType
from Entity import _RawTextPair as RawTextPair
from Entity import _Detection as Detection
from Entity import _RawTextExcerptLocation as RawTextExcerptLocation
from Entity import _EnumYesNo as EnumYesNo
from Entity import _PlagiarismObfuscation as PlagiarismObfuscation
from Entity import _PlagiarismType as PlagiarismType
from Repository import _TextCollectionMetaRepository as TextCollectionMetaRepository
from Repository import _RawTextRepository as RawTextRepository
from Repository import _RawTextPairRepository as RawTextPairRepository
from Repository import _RawTextExcerptLocationRepository as RawTextExcerptLocationRepository
from Repository import _DetectionRepository as DetectionRepository
from Repository import _PanRepository as PanRepository
from Constant import _Pan as PanConstant
import os

class DataImportationProcess(object):

    def Hello(self):
        print ('Hello, I\'m the DataImportationProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')

    def ImportFromPanFiles(self, textCollectionMeta, folderCompletePath):
        # overview: 
        #  create dataBaseId,
        #  save rawTexts, 
        #  import pairs relationships,
        #  import detections relationships.
        textCollectionMetaId = self.SaveTextCollection(textCollectionMeta = textCollectionMeta)
        rawTextList = self.GetRawTexts(
            folderCompletePath = folderCompletePath, 
            textCollectionMetaId = textCollectionMetaId)
        self.SaveRawTextList(rawTextList = rawTextList)
        rawTextPairList = self.GetRawTextPairs(
            folderCompletePath = folderCompletePath, 
            textCollectionMetaId = textCollectionMetaId)
        self.SaveRawTextPairList(rawTextPairList = rawTextPairList)

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

    def GetRawTextPairs(self, folderCompletePath, textCollectionMetaId):
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

    _textCollectionMetaRepository = TextCollectionMetaRepository()
    _rawTextRepository = RawTextRepository()
    _rawTextPairRepository = RawTextPairRepository()
    _rawTextExcerptLocationRepository = RawTextExcerptLocationRepository()
    _detectionRepository = DetectionRepository()
    _panRepository = PanRepository()

    def __init__(self):
        pass
