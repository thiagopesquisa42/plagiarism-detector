from itertools import groupby
import math

from Process import _BaseProcess as BaseProcess
from Entity.Seeding import _SeedingData as SeedingData
from Entity.Seeding import _Seed as Seed
from Entity.Seeding import _SeedAttributes as SeedAttributes
from Entity import _PlagiarismClass as PlagiarismClass
from Repository import _BaseRepository as BaseRepository
from Repository.PreProcessing import _PreProcessedDataRepository as PreProcessedDataRepository
from Repository.PreProcessing.TextStructure import _SentenceListRepository as SentenceListRepository
from Repository import _RawTextPairRepository as RawTextPairRepository
from Repository.Seeding import _SeedRepository as SeedRepository
from Repository.Seeding import _SeedingDataRepository as SeedingDataRepository
from Repository.Seeding import _SeedAttributesRepository as SeedAttributesRepository
from Repository import _DetectionRepository as DetectionRepository
from constant import Threshold

class SeedingProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from SeedingProcess')
        print ('Hello, I\'m the SeedingProcess')

    def SeedingProcessing(self, preProcessedDataId, seedingData):
        try:
            self.logger.info('Seeding Processing started')

            # self.logger.info('create Seeding Data Instance')
            # preProcessedData = self._preProcessedDataRepository.Get(id = preProcessedDataId)
            # seedingData = self.CreateSeedingData(preProcessedData)

            # self.logger.info('create seeds candidates')
            rawTextPairList = self._rawTextPairRepository.GetListByTextCollectionMeta(seedingData.preProcessedData.textCollectionMeta)
            # self.CreateSeedCandidateListFromRawTextPairList(seedingData, rawTextPairList)

            # [0] Create seeds candidates from 
            #   all possible sentences suspicious-source-pairs in preprocessedData
            # self.logger.info('create seeds attributes registers')
            # self.CreateAttributesDefaultRegisterForSeeds(
            #     seedingData = seedingData)
            
            # [1] Fill class (no-plag, obfuscated-plag...)
            self.logger.info('label seeds detected')
            self.LabelSeedList(seedingData, rawTextPairList)

            # [2] Calculate attributes over bag-of-words and locations from both sentences
            self.logger.info('calculate seeds attributes')
            self.CalculateAttributesSeedList(seedingData, rawTextPairList)

        except Exception as exception:
            self.logger.info('Seeding Processing failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Seeding Processing finished')
            return seedingData
    
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
            Seed(seedingDataId = seedingData.id,
                suspiciousSentenceId = suspiciousSentence.id,
                sourceSentenceId = sourceSentence.id,
                rawTextPairId = rawTextPair.id)
            for suspiciousSentence in suspiciousSentenceList.sentences
            for sourceSentence in sourceSentenceList.sentences]
        self._seedRepository.InsertByRawSql(seedCandidateList)

    def CreateAttributesDefaultRegisterForSeeds(self, seedingData):
        seedIdList = self._seedRepository.GetRawListIdsBySeedingData(seedingData)
        self._seedAttributesRepository.InsertDefaultListByRawSql(seedIdList = seedIdList)
    #end_region [Create seeds candidates]

    #region [Fill seeds plagiarism class]
    def LabelSeedList(self, seedingData, rawTextPairList):
        commitList = []
        for rawTextPair in rawTextPairList:
            seedList = self._seedRepository.GetListByRawTextPair(rawTextPair, seedingData)
            seedList = self.LabelAllSeedAsNone(seedList)
            seedDetectedSet = self.LabelSeedAsDetection(seedList, rawTextPair)
            seedList = set(seedList)
            seedList.update(seedDetectedSet)
            commitList.extend(seedList)
        self._baseRepository.InsertList(commitList)

    def LabelAllSeedAsNone(self, seedList):
        for seed in seedList:
            seed.attributes.plagiarismClass = PlagiarismClass.none
        return seedList

    def LabelSeedAsDetection(self, seedList, rawTextPair):
        detectionList = self._detectionRepository.GetByRawTextPair(rawTextPair)
        if(detectionList is None or len(detectionList) == 0):
            return set()
        seedDetectedSet = self.GetSeedsInsideAnyDetection(detectionList, seedList)
        return seedDetectedSet

    def GetSeedsInsideAnyDetection(self, detectionList, seedList):
        seedSortedList = self.SortSeedListBySuspiciousSourceLocation(seedList)
        seedMatrixLineSuspiciousColumnSource = SeedingProcess.GetMatrixLineSuspiciousColumnSource(seedSortedList)
        seedDetectedSet = set()
        for detection in detectionList:
            seedDetectedList = self.GetSeedListInDetection(
                seedMatrixLineSuspiciousColumnSource, 
                detection)
            for seed in seedDetectedList:
                seed.attributes.plagiarismClass = PlagiarismClass.FromPlagiarismObfuscation(detection.obfuscation)
            seedDetectedSet.update(seedDetectedList)
        return seedDetectedSet

    def SortSeedListBySuspiciousSourceLocation(self, seedList):
        return sorted(seedList, 
            key = lambda seed:
                (
                    SeedingProcess.GetSuspiciousLocation(seed)[0],
                    SeedingProcess.GetSourceLocation(seed)[0]))

    def GetSuspiciousLocation(seed):
        return (seed.suspiciousSentence.rawTextExcerptLocation.firstCharacterPosition,
            seed.suspiciousSentence.rawTextExcerptLocation.lastCharacterPosition)

    def GetSourceLocation(seed):
        return (seed.sourceSentence.rawTextExcerptLocation.firstCharacterPosition,
            seed.sourceSentence.rawTextExcerptLocation.lastCharacterPosition)

    def GetMatrixLineSuspiciousColumnSource(seedList):
        seedMatrixLineSuspiciousColumnSource = [
            (
                location[0], 
                location[1],
                [(
                    seed.sourceSentence.rawTextExcerptLocation.firstCharacterPosition, 
                    seed.sourceSentence.rawTextExcerptLocation.lastCharacterPosition, 
                    seed) for seed in seedListIterator])
            for location, seedListIterator in groupby(seedList, SeedingProcess.GetSuspiciousLocation)]
        return seedMatrixLineSuspiciousColumnSource

    def GetSeedListInDetection(self, seedMatrixLineSuspiciousColumnSource, detection):
        detectionSuspiciousFirstPosition = detection.rawTextSuspiciousLocation.firstCharacterPosition
        detectionSuspiciousLastPosition = detection.rawTextSuspiciousLocation.lastCharacterPosition
        detectionSourceFirstPosition = detection.rawTextSourceLocation.firstCharacterPosition
        detectionSourceLastPosition = detection.rawTextSourceLocation.lastCharacterPosition
        seedDetectedMatrix = [
            [seed 
                for sourceFirstPosition, sourceLastPosition, seed in suspiciousLine
                if(SeedingProcess.SentenceIsInDetection(
                    sourceFirstPosition, sourceLastPosition,
                    detectionSourceFirstPosition, detectionSourceLastPosition))]
            for suspiciousFirstPosition, suspiciousLastPosition, suspiciousLine in seedMatrixLineSuspiciousColumnSource
            if(SeedingProcess.SentenceIsInDetection(
                suspiciousFirstPosition, suspiciousLastPosition, 
                detectionSuspiciousFirstPosition, detectionSuspiciousLastPosition))]
        seedDetectedList = []
        [seedDetectedList.extend(seedList)
            for seedList in seedDetectedMatrix]
        return seedDetectedList

    def SentenceIsInDetection(sentenceFirstPosition, sentenceLastPosition, 
        detectionFirstPosition, detectionLastPosition):
        threshold = Threshold.DETECTION_MINIMUM_PERCENTUAL_INTERSECTION
        percentageInDetection = SeedingProcess.SentencePercentageInDetection(
            sentenceFirstPosition, sentenceLastPosition, detectionFirstPosition, detectionLastPosition)
        isIn = percentageInDetection > threshold
        return isIn
    
    def SentencePercentageInDetection(sentenceFirstPosition, sentenceLastPosition, 
        detectionFirstPosition, detectionLastPosition):
        sentenceLength = sentenceLastPosition - sentenceFirstPosition
        overlappedLength = min(detectionLastPosition, sentenceLastPosition) - max(detectionFirstPosition, sentenceFirstPosition)
        percentageInDetection = overlappedLength / sentenceLength
        return percentageInDetection
    #end_region [Fill seeds plagiarism class]    

    #region [Calculate attributes over seeds candidates]
    def CalculateAttributesSeedList(self, seedingData, rawTextPairList):
        commitList = []
        for rawTextPair in rawTextPairList:
            seedList = self._seedRepository.GetListByRawTextPair(rawTextPair, seedingData)
            seedList = self.CalculateSeedListCosine(seedList)
            seedList = self.CalculateSeedListDice(seedList)
            seedList = self.CalculateSeedListMetaCosineAttributes(seedList)
            seedList = self.CalculateSeedListMetaDiceAttributes(seedList)
            seedList = self.CalculateLengthRatio(seedList)
            commitList.extend(seedList)
        self._baseRepository.InsertList(commitList)

    def CalculateSeedListCosine(self, seedList):
        for seed in seedList:  
            seed.attributes.cosine = SeedingProcess.Cosine(
                seed.suspiciousSentence.bagOfWords.wordOccurenceDictionary, 
                seed.sourceSentence.bagOfWords.wordOccurenceDictionary)
        return seedList

    def Cosine(dictionary1, dictionary2):
        scalarProduct = 0.0
        denominator =\
            SeedingProcess.EuclidianNormalize(dictionary1) *\
            SeedingProcess.EuclidianNormalize(dictionary2)
        if denominator == 0:
            return 0
        coocurrenceDicitionary = SeedingProcess.GetCoocurrenceDictionary(
            dictionary1, dictionary2)
        scalarProduct = sum([
            occurence1 * occurence2
            for occurence1, occurence2 in coocurrenceDicitionary.values()])
        cosine = scalarProduct/denominator
        return cosine
    
    def EuclidianNormalize(dictionary):
        squares = list(map(lambda value: value*value, dictionary.values()))
        _sum = sum(squares)
        euclidianNorm = math.sqrt(_sum)
        return euclidianNorm

    def GetCoocurrenceDictionary(dictionary1, dictionary2):
        keys1 = set(dictionary1.keys())
        keys2 = set(dictionary2.keys())
        commomKeys = keys1 & keys2
        coocurrenceDicitionary = {
            key: (dictionary1[key], dictionary2[key])
            for key in commomKeys}
        return coocurrenceDicitionary

    def CalculateSeedListDice(self, seedList):
        for seed in seedList:  
            seed.attributes.dice = SeedingProcess.Dice(
                seed.suspiciousSentence.bagOfWords.wordOccurenceDictionary, 
                seed.sourceSentence.bagOfWords.wordOccurenceDictionary)
        return seedList
    
    def Dice(dictionary1, dictionary2):
        dictionary1Binary = SeedingProcess.Binarize(dictionary1)
        dictionary2Binary = SeedingProcess.Binarize(dictionary2)
        euclidianNormDictionary1 = SeedingProcess.EuclidianNormalize(dictionary1Binary)
        euclidianNormDictionary2 = SeedingProcess.EuclidianNormalize(dictionary2Binary)
        denominator = euclidianNormDictionary1**2 + euclidianNormDictionary2**2

        coocurrenceDictionary = SeedingProcess.GetCoocurrenceDictionary(
            dictionary1Binary, dictionary2Binary)
        scalarProduct = sum([
            occurence1 * occurence2
            for occurence1, occurence2 in coocurrenceDictionary.values()])
        dice = 2*scalarProduct/denominator
        return dice

    def Binarize(dictionary):
        return {
            key: value != 0
            for key, value in dictionary.items()}

    def CalculateSeedListMetaCosineAttributes(self, seedList):
        seedMatrix = SeedingProcess.GetMatrixLineSuspiciousColumnSource(seedList)
        cosineMatrix = [
            [seed.attributes.cosine 
                for sourceFirstPosition, sourceLastPosition, seed in seedListSameSuspicious]
            for suspiciousFirstPosition, suspiciousLastPosition, seedListSameSuspicious in seedMatrix]
        maxCosineList = [max(cosineList) for cosineList in cosineMatrix]
        meanMaxCosine = sum(maxCosineList)/float(len(maxCosineList))
        for suspiciousIndex,\
            (suspiciousFirstPosition, suspiciousLastPosition, seedListSameSuspicious)\
            in enumerate(seedMatrix):
            maxCosineNeighbour = SeedingProcess.CalculateMaxNeighbour(suspiciousIndex, maxCosineList)
            verticalCosineMaxMeasures = SeedingProcess.CalculateVerticalMaxMeasures(suspiciousIndex, maxCosineList, cosineMatrix)
            for sourceIndex,\
                (sourceFirstPosition, sourceLastPosition, seed)\
                in enumerate(seedListSameSuspicious):
                seed.attributes.isMaxCosine = (seed.attributes.cosine == maxCosineList[suspiciousIndex])
                seed.attributes.maxCosineDiff = maxCosineList[suspiciousIndex] - seed.attributes.cosine
                seed.attributes.meanMaxCosineDiff = meanMaxCosine - seed.attributes.cosine
                seed.attributes.maxCosineNeighbour = maxCosineNeighbour
                seed.attributes.verticalCosineMaxDistance = verticalCosineMaxMeasures[0]
                seed.attributes.verticalCosineMaxMeasure = verticalCosineMaxMeasures[1]
        return seedList

    def CalculateMaxNeighbour(suspiciousIndex, maxValuesList):
        if(len(maxValuesList) == 1):
            return None
        if(suspiciousIndex == 0):
            return maxValuesList[suspiciousIndex + 1]
        if(suspiciousIndex + 1 == len(maxValuesList)):
            return maxValuesList[suspiciousIndex - 1]
        return max(
            maxValuesList[suspiciousIndex - 1],
            maxValuesList[suspiciousIndex + 1])
    
    def CalculateVerticalMaxMeasures(suspiciousIndex, maxValuesList, matrix):
        valueListSameSuspicious = matrix[suspiciousIndex]
        if(len(valueListSameSuspicious) == 1 or len(matrix) == 1):
            return (None, None)
        maxValue = maxValuesList[suspiciousIndex]
        normalizedVerticalIndexMaxValue = [
            index/(len(valueListSameSuspicious) - 1)
            for index, cosine in enumerate(valueListSameSuspicious)
            if(cosine == maxValue)][0]
        normalizedSuspiciousIndex = suspiciousIndex/(len(matrix) - 1)
        verticalMaxMeasure = normalizedVerticalIndexMaxValue - normalizedSuspiciousIndex
        verticalMaxDistance = abs(verticalMaxMeasure)
        return (verticalMaxDistance, verticalMaxMeasure)

    def CalculateSeedListMetaDiceAttributes(self, seedList):
        seedMatrix = SeedingProcess.GetMatrixLineSuspiciousColumnSource(seedList)
        diceMatrix = [
            [seed.attributes.dice 
                for sourceFirstPosition, sourceLastPosition, seed in seedListSameSuspicious]
            for suspiciousFirstPosition, suspiciousLastPosition, seedListSameSuspicious in seedMatrix]
        maxDiceList = [max(diceList) for diceList in diceMatrix]
        meanMaxDice = sum(maxDiceList)/float(len(maxDiceList))
        for suspiciousIndex,\
            (suspiciousFirstPosition, suspiciousLastPosition, seedListSameSuspicious)\
            in enumerate(seedMatrix):
            maxDiceNeighbour = SeedingProcess.CalculateMaxNeighbour(suspiciousIndex, maxDiceList)
            verticalDiceMaxMeasures = SeedingProcess.CalculateVerticalMaxMeasures(suspiciousIndex, maxDiceList, diceMatrix)
            for sourceIndex,\
                (sourceFirstPosition, sourceLastPosition, seed)\
                in enumerate(seedListSameSuspicious):
                seed.attributes.isMaxDice = (seed.attributes.dice == maxDiceList[suspiciousIndex])
                seed.attributes.maxDiceDiff = maxDiceList[suspiciousIndex] - seed.attributes.dice
                seed.attributes.meanMaxDiceDiff = meanMaxDice - seed.attributes.dice
                seed.attributes.maxDiceNeighbour = maxDiceNeighbour
                seed.attributes.verticalDiceMaxDistance = verticalDiceMaxMeasures[0]
                seed.attributes.verticalDiceMaxMeasure = verticalDiceMaxMeasures[1]
        return seedList
    
    def CalculateLengthRatio(self, seedList):
        lengthRatioList = [
            (seed.suspiciousSentence.rawTextExcerptLocation.stringLength /
                seed.sourceSentence.rawTextExcerptLocation.stringLength)
            for seed in seedList]
        for index, seed in enumerate(seedList):  
            seed.attributes.lengthRatio = lengthRatioList[index]
        return seedList
    #end_region [Calculate attributes over seeds candidates]
    
    _baseRepository = BaseRepository()
    _preProcessedDataRepository = PreProcessedDataRepository()
    _rawTextPairRepository = RawTextPairRepository()
    _sentenceListRepository = SentenceListRepository()
    _seedRepository = SeedRepository()
    _detectionRepository = DetectionRepository()
    _seedingDataRepository = SeedingDataRepository()
    _seedAttributesRepository = SeedAttributesRepository()

    def __init__(self):
        super().__init__()
