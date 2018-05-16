from Process import _BaseProcess as BaseProcess
from Entity.Seeding import _SeedingData as SeedingData
from Entity.Seeding import _Seed as Seed
from Repository import _BaseRepository as BaseRepository
from Repository.PreProcessing import _PreProcessedDataRepository as PreProcessedDataRepository
from Repository.PreProcessing.TextStructure import _SentenceListRepository as SentenceListRepository
from Repository import _RawTextPairRepository as RawTextPairRepository

class SeedingProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from SeedingProcess')
        print ('Hello, I\'m the SeedingProcess')

    def SeedingProcessing(self, preProcessedDataId):
        try:
            self.logger.info('Seeding Processing started')

            self.logger.info('create Seeding Data Instance')
            preProcessedData = self._preProcessedDataRepository.Get(id = preProcessedDataId)
            seedingData = self.CreateSeedingData(preProcessedData)

            self.logger.info('create seeds candidates')
            rawTextPairList = self._rawTextPairRepository.GetListByTextCollectionMeta(preProcessedData.textCollectionMeta)
            self.CreateSeedCandidateListFromRawTextPairList(seedingData, rawTextPairList)

            print('')
            # [0] Create seeds candidates from 
            #   all possible sentences suspicious-source-pairs in preprocessedData
            # [1] Fill class (no-plag, obfuscated-plag...)
            # [2] Calculate attributes over bag-of-words and locations from both sentences

        except Exception as exception:
            self.logger.info('Seeding Processing failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Seeding Processing finished')
    
    #region [Create seeding data]
    def CreateSeedingData(self, preProcessedData):
        seedingData = SeedingData(
            preProcessedData = preProcessedData,
            description = 'em testes')
        self._baseRepository.Insert(seedingData)
        return seedingData
    #end_region [Create seeding data]

    #region [Create seeds candidates]
    def CreateSeedCandidateListFromRawTextPairList(self, seedingData, rawTextPairList):
        for rawTextPair in rawTextPairList:
            self.CreateSeedCandidateList(seedingData, rawTextPair)
    
    def CreateSeedCandidateList(self, seedingData, rawTextPair):
        suspiciousSentenceList = self._sentenceListRepository.GetByRawText(
            rawText = rawTextPair.suspiciousRawText, 
            preProcessedData = seedingData.preProcessedData)
        sourceSentenceList = self._sentenceListRepository.GetByRawText(
            rawText = rawTextPair.sourceRawText, 
            preProcessedData = seedingData.preProcessedData)
        seedCandidateList = [
            Seed(seedingData = seedingData,
                suspiciousSentence = suspiciousSentence,
                sourceSentence = sourceSentence,
                rawTextPair = rawTextPair)
            for suspiciousSentence in suspiciousSentenceList.sentences
            for sourceSentence in sourceSentenceList.sentences]
        self._baseRepository.InsertList(seedCandidateList)
    #end_region [Create seeds candidates]

    _baseRepository = BaseRepository()
    _preProcessedDataRepository = PreProcessedDataRepository()
    _rawTextPairRepository = RawTextPairRepository()
    _sentenceListRepository = SentenceListRepository()

    def __init__(self):
        super().__init__()
