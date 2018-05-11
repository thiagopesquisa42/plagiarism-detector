import re
from collections import Counter

import nltk

from constant import StopWord
from Entity.PreProcessing import _PreProcessedData as PreProcessedData
from Entity.PreProcessing import _PreProcessStep as PreProcessStep
from Entity.PreProcessing import _PreProcessStepChainNode as PreProcessStepChainNode
from Entity.PreProcessing import _RawTextExcerptLocation as RawTextExcerptLocation
from Entity.PreProcessing.Algorithm import _Tokenization as Tokenization
from Entity.PreProcessing.Algorithm import _TokenizationAlgorithm as TokenizationAlgorithm
from Entity.PreProcessing.Algorithm import _TokenizationType as TokenizationType
from Entity.PreProcessing.Algorithm import _ToLower as ToLower
from Entity.PreProcessing.TextStructure import _Sentence as Sentence
from Entity.PreProcessing.TextStructure import _SentenceList as SentenceList
from Process import _BaseProcess as BaseProcess
from Repository import _RawTextExcerptLocationRepository as RawTextExcerptLocationRepository
from Repository import _RawTextRepository as RawTextRepository
from Repository.PreProcessing import _PreProcessedDataRepository as PreProcessedDataRepository
from Repository.PreProcessing import _PreProcessStepChainNodeRepository as PreProcessStepChainNodeRepository
from Repository.PreProcessing import _PreProcessStepRepository as PreProcessStepRepository
from Repository.PreProcessing.TextStructure import _SentenceListRepository as SentenceListRepository
from Repository.PreProcessing.TextStructure import _SentenceRepository as SentenceRepository


class PreProcessingRawTextProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from PreProcessingRawTextProcess')
        print ('Hello, I\'m the PreProcessingRawTextProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')
        self._rawTextInternalProcess.Hello()

    def PreProcessing(self, textCollectionMetaId):
        try:
            self.logger.info('PreProcessing started')
            #preProcessedData = self.CreatePreProcessedDataIdentifier()
            #rawTextList = self._rawTextRepository.GetByTextCollectionMetaId(textCollectionMetaId)
            #self.TokenizeInSentences(rawTextList, preProcessedData)
            preProcessedData = self._preProcessedDataRepository.Get(id = 8)
            self.ToLowerSentenceListGroup(preProcessedData)

            # [Z]
            # 1. create data base preprocessed id [ok]
            # 2. create pp-step-chain node
            # 3. store pp-step configuration of the node
            # 4. store pp-step-chain node
            # 5. start tokenize in sentences step 
            # 6. for each raw text, create a sentence list

            # [A]
            # repeat 2 to 4 plus
            # 7. start lower step
            # 8. for each sentence in sentence-list from previous step-node
            #      create another sentence passed by the pp-step
            # 

        except Exception as exception:
            self.logger.info('PreProcessing failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('PreProcessing finished')

    def CreatePreProcessedDataIdentifier(self):
        preProcessedData = PreProcessedData()
        self._preProcessedDataRepository.Insert(preProcessedData)
        return preProcessedData
    
    def TokenizeInSentences(self, rawTextList, preProcessedData):
        preProcessStep = self.CreateTokenizationStep(
            tokenizationType = TokenizationType.SENTENCE, 
            tokenizationAlgorithm = TokenizationAlgorithm.PUNKT_EN, description = 'em testes')
        preProcessStepChainNode = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        for rawText in rawTextList:
            sentenceList = self.CreateSentenceListFromRawText(rawText, preProcessStepChainNode)
            self.CreateSentencesByPunktTokenizer(rawText, sentenceList)
    
    def ToLowerSentenceListGroup(self, preProcessedData):
        preProcessStep = self.CreateToLowerStep(description = 'em testes')
        preProcessStepChainNode = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        previousSentenceListGroup = self._sentenceListRepository.GetByPreProcessStepChainNode(
            preProcessStepChainNode.previousPreProcessStepChainNode)
        for previousSentenceList in previousSentenceListGroup:
            sentenceList = SentenceList(
                rawTextExcerptLocation = previousSentenceList.rawTextExcerptLocation,
                preProcessStepChainNode = preProcessStepChainNode)
            self.ToLowerSentences(sentenceList, previousSentenceList)
            
    def CreateTokenizationStep(self, tokenizationType, tokenizationAlgorithm, description = None):
        tokenization = Tokenization(
            _type = tokenizationType,
            algorithm = tokenizationAlgorithm, 
            description = description)
        preProcessStep = PreProcessStep(algorithm = tokenization.ToDictionary())
        self._preProcessStepRepository.Insert(preProcessStep)
        return preProcessStep
    
    def CreateToLowerStep(self, description = None):
        toLower = ToLower(description = description)
        preProcessStep = PreProcessStep(algorithm = toLower.ToDictionary())
        self._preProcessStepRepository.Insert(preProcessStep)
        return preProcessStep

    def AddPreProcessStepToStepChain(self, preProcessedData, preProcessStep):
        previousPreProcessStepChainNode = preProcessedData.topPreProcessStepChainNode
        preProcessStepChainNode = PreProcessStepChainNode(
            preProcessedData = preProcessedData,
            preProcessStep = preProcessStep,
            previousPreProcessStepChainNode = previousPreProcessStepChainNode,
            stepPosition = 0 if(previousPreProcessStepChainNode == None) else previousPreProcessStepChainNode.stepPosition + 1)
        self._preProcessStepChainNodeRepository.Insert(preProcessStepChainNode)
        preProcessedData.topPreProcessStepChainNodeId = preProcessStepChainNode.id
        self._preProcessedDataRepository.Update(preProcessedData)
        return preProcessStepChainNode
    
    def CreateSentenceListFromRawText(self, rawText, preProcessStepChainNode):
        sentenceList = SentenceList(
            preProcessStepChainNode = preProcessStepChainNode,
            rawTextExcerptLocation = self.CreateLocationEntireRawText(rawText))
        self._sentenceListRepository.Insert(sentenceList)
        return sentenceList

    def CreateLocationEntireRawText(self, rawText):
        rawTextExcerptLocation = RawTextExcerptLocation(
            firstCharacterPosition = 0,
            stringLength = len(rawText.text),
            rawText = rawText)
        self._rawTextExcerptLocationRepository.Insert(rawTextExcerptLocation)
        return rawTextExcerptLocation

    def CreateSentencesByPunktTokenizer(self, rawText, sentenceList):
        sentenceDetector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentenceRawTextExcerptLocationList = [
            RawTextExcerptLocation(
                firstCharacterPosition = firstCharacterPosition,
                rawTextId = rawText.id,
                stringLength = lastCharacterPosition - firstCharacterPosition)
            for (firstCharacterPosition, lastCharacterPosition) in sentenceDetector.span_tokenize(rawText.text)]
        sentenceTextList = sentenceDetector.tokenize(rawText.text)
        sentences = []
        for index, text in enumerate(sentenceTextList):
            sentences.append(
                Sentence(
                    text = text,
                    rawTextExcerptLocation = sentenceRawTextExcerptLocationList[index],
                    sentenceList = sentenceList,
                    bagOfWords = None,
                    nGramsList = None))
        self._sentenceRepository.InsertList(sentences)
        return sentences

    def ToLowerSentences(self, sentenceList, previousSentenceList):
        sentences = []
        for previousSentence in previousSentenceList.sentences:
            sentences.append(
                Sentence(
                    text = previousSentence.text.lower(),
                    rawTextExcerptLocation = previousSentence.rawTextExcerptLocation,
                    sentenceList = sentenceList,
                    bagOfWords = None,
                    nGramsList = None))
        self._sentenceRepository.InsertList(sentences)

    _preProcessedDataRepository = PreProcessedDataRepository()
    _preProcessStepRepository = PreProcessStepRepository()
    _preProcessStepChainNodeRepository = PreProcessStepChainNodeRepository()
    _rawTextExcerptLocationRepository = RawTextExcerptLocationRepository()
    _rawTextRepository = RawTextRepository()
    _sentenceListRepository = SentenceListRepository()
    _sentenceRepository = SentenceRepository()

    def __init__(self):
        super().__init__()
