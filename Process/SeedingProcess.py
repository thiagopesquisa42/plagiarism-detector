from itertools import groupby
import math

from Process import _BaseProcess as BaseProcess
from Entity.Seeding import _SeedingData as SeedingData
from Entity.Seeding import _Seed as Seed
from Entity.Seeding import _SeedAttributes as SeedAttributes
from Entity.Seeding import _SeedListPerRawTextPair as SeedListPerRawTextPair
from Entity import _PlagiarismClass as PlagiarismClass
from Entity import _RawTextType as RawTextType
from Entity import _RawTextPair as RawTextPair
from Repository.PreProcessing import _PreProcessedDataRepository as PreProcessedDataRepository
from Repository.Seeding import _SeedingDataRepository as SeedingDataRepository
from constant import Threshold

class SeedingProcess(BaseProcess):

    def SeedingProcessing(self):
        try:
            self.logger.info('Seeding Processing started')

            self.logger.info('getting pre-processed-data')
            preProcessedData = self._preProcessedDataRepository.Get()
            self.logger.info('create seeding-data instance')
            seedingData = self.CreateSeedingData(preProcessedData)

            self.logger.info('create seeds candidates')
            seedingData = self.CreateSeedCandidateListFromPreProcessedData(seedingData, preProcessedData)
            seedingData = self._seedingDataRepository.StoreAndGet(seedingData)

            self.logger.info('label seeds detected')
            self.LabelSeedList(seedingData, detectionList = preProcessedData.textCollectionMeta.detectionList)
            seedingData = self._seedingDataRepository.StoreAndGet(seedingData)

            self.logger.info('calculate seeds attributes')
            self.CalculateAttributesSeedList(seedingData)
            seedingData = self._seedingDataRepository.StoreAndGet(seedingData)

        except Exception as exception:
            self.logger.exception('Seeding Processing failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Seeding Processing finished')
            return seedingData
    
    #region [Create seeding data]
    def CreateSeedingData(self, preProcessedData):
        listOfSeedListPerRawTextPair = [
            SeedListPerRawTextPair(rawTextPair = rawTextPair)
            for rawTextPair in preProcessedData.textCollectionMeta.rawTextPairList]
        seedingData = SeedingData(
            listOfSeedListPerRawTextPair = listOfSeedListPerRawTextPair)
        return self._seedingDataRepository.StoreAndGet(seedingData)
    #end_region [Create seeding data]

    #region [Create seeds candidates]
    def CreateSeedCandidateListFromPreProcessedData(self, seedingData, preProcessedData):
        for seedListPerRawTextPair in seedingData.listOfSeedListPerRawTextPair:
            suspiciousSentenceListPerRawText, sourceSentenceListPerRawText = self.GetPairOfSentenceListPerRawText(
                seedListPerRawTextPair.rawTextPair, preProcessedData.listOfSentenceList)
            if(suspiciousSentenceListPerRawText is None or 
                sourceSentenceListPerRawText is None):
                continue
            seedList = self.CreateSeedCandidateList(
                suspiciousSentenceListPerRawText, sourceSentenceListPerRawText)
            seedListPerRawTextPair.seedList = seedList
        return seedingData
    
    def GetPairOfSentenceListPerRawText(self, rawTextPair, listOfSentenceListPerRawText):
        suspiciousSentenceListPerRawText = next(
            (sentenceListPerRawText
                for sentenceListPerRawText in listOfSentenceListPerRawText
                if sentenceListPerRawText.rawText.fileName == rawTextPair.suspiciousRawText.fileName),
            None)
        sourceSentenceListPerRawText = next(
            (sentenceListPerRawText
                for sentenceListPerRawText in listOfSentenceListPerRawText
                if sentenceListPerRawText.rawText.fileName == rawTextPair.sourceRawText.fileName),
            None)
        return suspiciousSentenceListPerRawText, sourceSentenceListPerRawText

    def CreateSeedCandidateList(self, suspiciousSentenceListPerRawText, sourceSentenceListPerRawText):
        seedCandidateList = [
            Seed(suspiciousSentence = suspiciousSentence,
                sourceSentence = sourceSentence)
            for suspiciousSentence in suspiciousSentenceListPerRawText.sentences
            for sourceSentence in sourceSentenceListPerRawText.sentences]
        return seedCandidateList
    #end_region [Create seeds candidates]

    #region [Fill seeds plagiarism class]
    def LabelSeedList(self, seedingData, detectionList):
        for seedListPerRawTextPair in seedingData.listOfSeedListPerRawTextPair:
            _seedList = set(self.LabelAllSeedAsNone(
                seedList = seedListPerRawTextPair.seedList))
            _seedDetectedSet = set(self.LabelSeedAsDetection(seedListPerRawTextPair, detectionList))
            _seedList.update(_seedDetectedSet)
            seedListPerRawTextPair.seedList = list(_seedList)
        return seedingData

    def LabelAllSeedAsNone(self, seedList):
        for seed in seedList:
            seed.attributes.plagiarismClass = PlagiarismClass.none
        return seedList

    def LabelSeedAsDetection(self, seedListPerRawTextPair, detectionList):
        detectionListPerRawTextPair = self.GetDetectionListByRawTextPair(
            detectionList = detectionList, 
            rawTextPair =  seedListPerRawTextPair.rawTextPair)
        if(detectionListPerRawTextPair is None or len(detectionListPerRawTextPair) == 0):
            return set()
        seedDetectedSet = self.GetSeedsInsideAnyDetection(detectionListPerRawTextPair, seedListPerRawTextPair.seedList)
        return seedDetectedSet
    
    def GetDetectionListByRawTextPair(self, detectionList, rawTextPair):
        detectionListPerRawTextPair = [
            detection
            for detection in detectionList
            if(RawTextPair.isEqual(detection.rawTextPair, rawTextPair))]
        return detectionListPerRawTextPair

    def GetSeedsInsideAnyDetection(self, detectionList, seedList):
        seedMatrixLineSuspiciousColumnSource = SeedingProcess.GetMatrixLineSuspiciousColumnSource(seedList)
        seedDetectedSet = set()
        for detection in detectionList:
            seedDetectedList = self.GetSeedListInDetection(
                seedMatrixLineSuspiciousColumnSource, 
                detection)
            for seed in seedDetectedList:
                seed.attributes.plagiarismClass = PlagiarismClass.FromPlagiarismObfuscation(detection.obfuscation)
            seedDetectedSet.update(seedDetectedList)
        return seedDetectedSet

    def SortSeedListBySuspiciousSourceLocation(seedList):
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
        seedSortedList = SeedingProcess.SortSeedListBySuspiciousSourceLocation(seedList)        
        seedMatrixLineSuspiciousColumnSource = [
            (
                location[0], 
                location[1],
                [(
                    seed.sourceSentence.rawTextExcerptLocation.firstCharacterPosition, 
                    seed.sourceSentence.rawTextExcerptLocation.lastCharacterPosition, 
                    seed) for seed in seedListIterator])
            for location, seedListIterator in groupby(seedSortedList, SeedingProcess.GetSuspiciousLocation)]
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
        for seedList in seedDetectedMatrix:
            for seed in seedList:
                seed.detection = detection
            seedDetectedList.extend(seedList)
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
    def CalculateAttributesSeedList(self, seedingData):
        for seedListPerRawTextPair in seedingData.listOfSeedListPerRawTextPair:
            seedListPerRawTextPair.seedList = self.CalculateSeedListCosine(seedListPerRawTextPair.seedList)
            seedListPerRawTextPair.seedList = self.CalculateSeedListDice(seedListPerRawTextPair.seedList)
            seedListPerRawTextPair.seedList = self.CalculateSeedListMetaCosineAttributes(seedListPerRawTextPair.seedList)
            seedListPerRawTextPair.seedList = self.CalculateSeedListMetaDiceAttributes(seedListPerRawTextPair.seedList)
            seedListPerRawTextPair.seedList = self.CalculateLengthRatio(seedListPerRawTextPair.seedList)
        return seedingData

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
    
    def __init__(self, context):
        self._seedingDataRepository = SeedingDataRepository(context)
        self._preProcessedDataRepository = PreProcessedDataRepository(context)
        super().__init__()
