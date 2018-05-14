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
from Entity.PreProcessing.TextStructure import _BagOfWords as BagOfWords
from Process import _BaseProcess as BaseProcess
from Repository import _RawTextExcerptLocationRepository as RawTextExcerptLocationRepository
from Repository import _RawTextRepository as RawTextRepository
from Repository.PreProcessing import _PreProcessedDataRepository as PreProcessedDataRepository
from Repository.PreProcessing import _PreProcessStepChainNodeRepository as PreProcessStepChainNodeRepository
from Repository.PreProcessing import _PreProcessStepRepository as PreProcessStepRepository
from Repository.PreProcessing.TextStructure import _SentenceListRepository as SentenceListRepository
from Repository.PreProcessing.TextStructure import _SentenceRepository as SentenceRepository
from Repository.PreProcessing.TextStructure import _BagOfWordsRepository as BagOfWordsRepository

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
            # preProcessedData = self.CreatePreProcessedDataIdentifier()
            # rawTextList = self._rawTextRepository.GetByTextCollectionMetaId(textCollectionMetaId)
            # self.TokenizeRawTextInSentences(rawTextList, preProcessedData)
            # self.ToLowerSentenceListGroup(preProcessedData)
            preProcessedData = self._preProcessedDataRepository.Get(id = 11)
            self.TokenizeSentenceListGroupInBagOfWords(preProcessedData)

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

            # [D]
            # repeat 2 to 4 plus
            # 7. start tokenize in words step
            # 8. for each sentence in sentence-list from previous step-node
            #       create another sentence passed by the pp-step
            #       create BoW from the tokenized words

        except Exception as exception:
            self.logger.info('PreProcessing failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('PreProcessing finished')

    def CreatePreProcessedDataIdentifier(self):
        preProcessedData = PreProcessedData()
        self._preProcessedDataRepository.Insert(preProcessedData)
        return preProcessedData
    
    def TokenizeRawTextInSentences(self, rawTextList, preProcessedData):
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
            self._sentenceListRepository.Insert(sentenceList)
            self.ToLowerSentences(previousSentenceList, sentenceList)

    def TokenizeSentenceListGroupInBagOfWords(self, preProcessedData):
        preProcessStep = self.CreateTokenizationStep(
            tokenizationType = TokenizationType.WORD, 
            tokenizationAlgorithm = TokenizationAlgorithm.TREEBANK_WORD_TOKENIZER, 
            description = 'em testes')
        preProcessStepChainNode = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        previousSentenceListGroup = self._sentenceListRepository.GetByPreProcessStepChainNode(
            preProcessStepChainNode.previousPreProcessStepChainNode)
        for previousSentenceList in previousSentenceListGroup:
            sentenceList = SentenceList(
                rawTextExcerptLocation = previousSentenceList.rawTextExcerptLocation,
                preProcessStepChainNode = preProcessStepChainNode)
            self._sentenceListRepository.Insert(sentenceList)
            self.TokenizeSentencesInBagOfWords(previousSentenceList, sentenceList)

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

    def ToLowerSentences(self, previousSentenceList, sentenceList):
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

    def TokenizeSentencesInBagOfWords(self, previousSentenceList, sentenceList):
        sentences = []
        for previousSentence in previousSentenceList.sentences:
            sentences.append(
                Sentence(
                    text = previousSentence.text,
                    rawTextExcerptLocation = previousSentence.rawTextExcerptLocation,
                    sentenceList = sentenceList,
                    bagOfWords = None,
                    nGramsList = None))
        self._sentenceRepository.InsertList(sentences)
        self.CreateBagOfWordsByTreeBankWordTokenizer(sentences)

    def CreateBagOfWordsByTreeBankWordTokenizer(self, sentences):
        listOfbagOfWords = []
        wordTokenizer = nltk.TreebankWordTokenizer()
        for sentence in sentences:
            wordsSimpleList = wordTokenizer.tokenize(sentence.text)
            wordOccurenceDictionary = Counter(wordsSimpleList)
            bagOfWords = BagOfWords(
                sentence = sentence,
                wordOccurenceDictionary = wordOccurenceDictionary)
            listOfbagOfWords.append(bagOfWords)
        self._bagOfWordsRepository.InsertList(listOfbagOfWords)
        sentencesWithBagOfWordReference = []
        for bagOfWords in listOfbagOfWords:
            sentence = bagOfWords.sentence
            sentence.bagOfWords = bagOfWords
            sentencesWithBagOfWordReference.append(sentence)
        self._sentenceRepository.UpdateList(sentencesWithBagOfWordReference)
        
    _preProcessedDataRepository = PreProcessedDataRepository()
    _preProcessStepRepository = PreProcessStepRepository()
    _preProcessStepChainNodeRepository = PreProcessStepChainNodeRepository()
    _rawTextExcerptLocationRepository = RawTextExcerptLocationRepository()
    _rawTextRepository = RawTextRepository()
    _sentenceListRepository = SentenceListRepository()
    _sentenceRepository = SentenceRepository()
    _bagOfWordsRepository = BagOfWordsRepository()

    def __init__(self):
        super().__init__()
