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

class DataImportationProcess(object):

    def Hello(self):
        print ('Hello, I\'m the DataImportationProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')
        self._tokenInternalProcess.Hello()
        self._rawTextInternalProcess.Hello()
        self._rawTextInternalProcess.TestInsertARawText()

    def ImportFromPanFiles(self, folderCompletePath, dataBaseCreationDate):
        tcm = TextCollectionMeta(creationDate = '2014-05-14', description = 'pan14-text-alignment-test-corpus3-2014-05-14', sourceUrl = None, name = 'base do Pan 2014')        
        self._textCollectionMetaRepository.Insert(textCollectionMeta = tcm)
        
        rt = RawText(_type = RawTextType.suspicious, 
                    textCollectionMetaId = tcm.id,
                    text = 'Este é um texto de teste!!',
                    fileName = 'text/random/susp00043.txt')
        self._rawTextRepository.Insert(rawText = rt)
        rt2 = self._rawTextRepository.Get(id = rt.id)
        print(rt2.id, rt2.textCollectionMetaId, rt2.text, rt2.fileName, rt2.textCollectionMeta.name)
        rt3 = RawText(_type = RawTextType.suspicious, 
                    textCollectionMetaId = tcm.id,
                    text = 'E este é outro texto de teste.',
                    fileName = 'text/src/src00564.txt')
        self._rawTextRepository.Insert(rawText = rt3)
        print(rt3.id)

        rtp = RawTextPair(suspiciousRawTextId = rt3.id, sourceRawTextId = rt.id)
        self._rawTextPairRepository.Insert(rawTextPair = rtp)

        rtel = RawTextExcerptLocation(firstCharacterPosition = 0, stringLength = 10,
            rawTextId = rt3.id, preProcessedDataId = None)
        rtel2 = RawTextExcerptLocation(firstCharacterPosition = 0, stringLength = 10,
            rawTextId = rt.id, preProcessedDataId = None)

        self._rawTextExcerptLocationRepository.Insert(rawTextExcerptLocation = rtel)
        self._rawTextExcerptLocationRepository.Insert(rawTextExcerptLocation = rtel2)

        d = Detection(_type = PlagiarismType.artificial, textCollectionMetaId = tcm.id,
            rawTextSuspiciousLocationId = rtel.id,
            rawTextSourceLocationId = rtel2.id,
            obfuscationDegree = 0.8967,
            obfuscation = PlagiarismObfuscation.none,
            name = 'plagiarism',
            isGiven = EnumYesNo.yes,
            isDetected = EnumYesNo.no)
        self._detectionRepository.Insert(detection = d)
        print('sucess!')

        
    _textCollectionMetaRepository = TextCollectionMetaRepository()
    _rawTextRepository = RawTextRepository()
    _rawTextPairRepository = RawTextPairRepository()
    _rawTextExcerptLocationRepository = RawTextExcerptLocationRepository()
    _detectionRepository = DetectionRepository()

    def __init__(self):
        pass