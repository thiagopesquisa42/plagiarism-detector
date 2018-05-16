import re
from collections import Counter
import nltk
from constant import StopWord
from constant import Threshold

from Entity.PreProcessing import _PreProcessedData as PreProcessedData
from Entity.PreProcessing import _PreProcessStep as PreProcessStep
from Entity.PreProcessing import _PreProcessStepChainNode as PreProcessStepChainNode
from Entity.PreProcessing import _RawTextExcerptLocation as RawTextExcerptLocation
from Entity.PreProcessing.Algorithm import _Tokenization as Tokenization
from Entity.PreProcessing.Algorithm import _TokenizationAlgorithm as TokenizationAlgorithm
from Entity.PreProcessing.Algorithm import _TokenizationType as TokenizationType
from Entity.PreProcessing.Algorithm import _ToLower as ToLower
from Entity.PreProcessing.Algorithm import _RemoveStopWords as RemoveStopWords
from Entity.PreProcessing.Algorithm import _FuseSentences as FuseSentences
from Entity.PreProcessing.Algorithm import _Stemmer as Stemmer
from Entity.PreProcessing.Algorithm import _StemmerAlgorithm as StemmerAlgorithm
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
            preProcessedData = self.CreatePreProcessedDataIdentifier(textCollectionMetaId)
            
            self.logger.info('Tokenize in Sentences')
            rawTextList = self._rawTextRepository.GetByTextCollectionMetaId(preProcessedData.textCollectionMetaId)
            self.TokenizeRawTextInSentences(rawTextList, preProcessedData)
            
            self.logger.info('To Lower')
            self.ToLowerSentenceListGroup(preProcessedData)
            
            self.logger.info('Tokenize in Words, create Bag-of-Words')
            self.TokenizeSentenceListGroupInBagOfWords(preProcessedData)
            
            self.logger.info('Remove stopwords from Bag-of-Words')
            self.RemoveStopWordsSentenceListGroup(preProcessedData)

            self.logger.info('Fuse small sentences')
            self.SentenceListGroupInnerFusion(preProcessedData)
            
            self.logger.info('Stem words from Bags-of-words')
            self.StemSentenceListGroup(preProcessedData)
            
        except Exception as exception:
            self.logger.info('PreProcessing failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('PreProcessing finished')

    def CreatePreProcessedDataIdentifier(self, textCollectionMetaId):
        preProcessedData = PreProcessedData(textCollectionMetaId = textCollectionMetaId)
        self._preProcessedDataRepository.Insert(preProcessedData)
        return preProcessedData
    
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
    
    #region [Tokenize raw text in sentences]
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

    def CreateTokenizationStep(self, tokenizationType, tokenizationAlgorithm, description = None):
        tokenization = Tokenization(
            _type = tokenizationType,
            algorithm = tokenizationAlgorithm, 
            description = description)
        preProcessStep = PreProcessStep(algorithm = tokenization.ToDictionary())
        self._preProcessStepRepository.Insert(preProcessStep)
        return preProcessStep
    
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
    #end_region [Tokenize raw text in sentences]

    #region [To lower sentences]
    def ToLowerSentenceListGroup(self, preProcessedData):
        preProcessStep = self.CreateToLowerStep(description = 'em testes')
        preProcessStepChainNode = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        sentenceListGroup = self._sentenceListRepository.GetByPreProcessStepChainNode(
            preProcessStepChainNode.previousPreProcessStepChainNode)
        for sentenceList in sentenceListGroup:
            sentenceList.preProcessStepChainNode = preProcessStepChainNode
            self.ToLowerSentences(sentenceList)
        self._sentenceListRepository.UpdateList(sentenceListGroup)

    def CreateToLowerStep(self, description = None):
        toLower = ToLower(description = description)
        preProcessStep = PreProcessStep(algorithm = toLower.ToDictionary())
        self._preProcessStepRepository.Insert(preProcessStep)
        return preProcessStep

    def ToLowerSentences(self, sentenceList):
        for sentences in sentenceList.sentences:
            sentences.text = sentences.text.lower()
        self._sentenceRepository.UpdateList(sentenceList.sentences)
    #end_region [To lower sentences]

    #region [Tokenize in words]
    def TokenizeSentenceListGroupInBagOfWords(self, preProcessedData):
        preProcessStep = self.CreateTokenizationStep(
            tokenizationType = TokenizationType.WORD, 
            tokenizationAlgorithm = TokenizationAlgorithm.TREEBANK_WORD_TOKENIZER, 
            description = 'em testes')
        preProcessStepChainNode = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        sentenceListGroup = self._sentenceListRepository.GetByPreProcessStepChainNode(
            preProcessStepChainNode.previousPreProcessStepChainNode)
        for sentenceList in sentenceListGroup:
            sentenceList.preProcessStepChainNode = preProcessStepChainNode
            self.TokenizeSentencesInBagOfWords(sentenceList)
        self._sentenceListRepository.UpdateList(sentenceListGroup)

    def TokenizeSentencesInBagOfWords(self, sentenceList):
        listOfBagOfWords = self.CreateBagOfWordsByTreeBankWordTokenizer(
            sentenceList.sentences)

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
        return listOfbagOfWords
    #end_region [Tokenize in words]

    #region [Remove stopwords from bag-of-words]
    def RemoveStopWordsSentenceListGroup(self, preProcessedData):
        stopWordList = StopWord.STOP_WORD_FULL_LIST
        preProcessStep = self.CreateStopWordStep(
            stopWordList = stopWordList,
            description = 'em testes')
        preProcessStepChainNode = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        sentenceListGroup = self._sentenceListRepository.GetByPreProcessStepChainNode(
            preProcessStepChainNode.previousPreProcessStepChainNode)
        for sentenceList in sentenceListGroup:
            sentenceList.preProcessStepChainNode = preProcessStepChainNode
            self.RemoveStopWordsFromSentences(sentenceList, stopWordList)
        self._sentenceListRepository.UpdateList(sentenceListGroup)

    def CreateStopWordStep(self, stopWordList, description = None):
        removeStopWords = RemoveStopWords(
            stopWordList = stopWordList, 
            description = description)
        preProcessStep = PreProcessStep(algorithm = removeStopWords.ToDictionary())
        self._preProcessStepRepository.Insert(preProcessStep)
        return preProcessStep

    def RemoveStopWordsFromSentences(self, sentenceList, stopWordList):
        for sentence in sentenceList.sentences:
            self.RemoveStopWordsFromBagOfWords(sentence.bagOfWords, stopWordList)
        self._sentenceRepository.UpdateList(sentenceList.sentences)

    def RemoveStopWordsFromBagOfWords(self, bagOfWords, stopWordList):
        bagOfWords.wordOccurenceDictionary = {
            word: occurence 
            for (word, occurence) in bagOfWords.wordOccurenceDictionary.items() 
            if word not in stopWordList}
    #end_region [Remove stopwords from bag-of-words]

    #region [fuse sentences and bag-of-words]
    def SentenceListGroupInnerFusion(self, preProcessedData):
        threshold = Threshold.SENTENCE_NUMBER_WORDS_TO_FUSE
        preProcessStep = self.CreateFuseSentenceStep(
            threshold = threshold, description = 'em testes')
        preProcessStepChainNode = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        sentenceListGroup = self._sentenceListRepository.GetByPreProcessStepChainNode(
            preProcessStepChainNode.previousPreProcessStepChainNode)
        for sentenceList in sentenceListGroup:
            sentenceList.preProcessStepChainNode = preProcessStepChainNode
            self.SentenceListInnerFusion(sentenceList, threshold)
        self._sentenceListRepository.UpdateList(sentenceListGroup)

    def CreateFuseSentenceStep(self, threshold, description = None):
        fuseSentences = FuseSentences(
            threshold = threshold, 
            description = description)
        preProcessStep = PreProcessStep(algorithm = fuseSentences.ToDictionary())
        self._preProcessStepRepository.Insert(preProcessStep)
        return preProcessStep

    def OrderAscendentSentencesByLocation(self, sentences):
        return sorted(sentences, 
            key = lambda sentence: (sentence.rawTextExcerptLocation.firstCharacterPosition))

    def SentenceListInnerFusion(self, _sentenceList, threshold):
        sentences = _sentenceList.sentences[:]
        if (len(sentences) == 0):
            return
        sortedSentences = self.OrderAscendentSentencesByLocation(sentences)
        deleteSentences = []
        newSentences = []
        newSentences.append(sortedSentences[0])
        for sentence in sortedSentences[1:]:
            sentenceNumberWords = sum(sentence.bagOfWords.wordOccurenceDictionary.values())
            if( sentenceNumberWords <= threshold):
                self.FuseWithLastSentence(newSentences, sentence)
                deleteSentences.append(sentence)
            else:
                newSentences.append(sentence)
        self._sentenceRepository.UpdateList(newSentences)
        self._sentenceRepository.BecomeOrphanList(deleteSentences)  

    def FuseWithLastSentence(self, sentenceList, sentence):
        if (len(sentenceList) == 0):
            raise Exception('Error fusing sentence into empty list')
        sentenceDestination = sentenceList[-1] #get last item from list
        sentenceDestination.rawTextExcerptLocation.stringLength +=\
            sentence.rawTextExcerptLocation.stringLength
        sentenceDestination.text += ' ' + sentence.text
        self.FuseBagOfWords(
            bagOfWordsDestination = sentenceDestination.bagOfWords,
            bagOfWords = sentence.bagOfWords)

    def FuseBagOfWords(self, bagOfWordsDestination, bagOfWords):
        destinationWordOccurenceDictionary = bagOfWordsDestination.wordOccurenceDictionary
        wordOccurenceDictionary = bagOfWords.wordOccurenceDictionary
        wordSimpleList = self.WordOccurenceDictionaryToWordList(
            destinationWordOccurenceDictionary)
        wordSimpleList.extend(self.WordOccurenceDictionaryToWordList(
            wordOccurenceDictionary))
        bagOfWordsDestination.wordOccurenceDictionary = Counter(wordSimpleList)

    def WordOccurenceDictionaryToWordList(self, wordOccurenceDictionary):
        wordSimpleList = []
        for word, occurence in wordOccurenceDictionary.items():
            wordSimpleList.extend([word for index in range(0, occurence)])
        return wordSimpleList
    #end_region [fuse sentences and bag-of-words]

    #region [stem words in bag-of-words]
    def StemSentenceListGroup(self, preProcessedData):
        preProcessStep = self.CreateStemmerStep(
            stemmerAlgorithm = StemmerAlgorithm.PORTER, description = 'em testes')
        preProcessStepChainNode = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        sentenceListGroup = self._sentenceListRepository.GetByPreProcessStepChainNode(
            preProcessStepChainNode.previousPreProcessStepChainNode)
        for sentenceList in sentenceListGroup:
            sentenceList.preProcessStepChainNode = preProcessStepChainNode
            self.StemsSentenceListByPorter(sentenceList)
        self._sentenceListRepository.UpdateList(sentenceListGroup)

    def CreateStemmerStep(self, stemmerAlgorithm, description = None):
        stemmer = Stemmer(
            algorithm = stemmerAlgorithm, 
            description = description)
        preProcessStep = PreProcessStep(algorithm = stemmer.ToDictionary())
        self._preProcessStepRepository.Insert(preProcessStep)
        return preProcessStep

    def StemsSentenceListByPorter(self, sentenceList):
        for sentence in sentenceList.sentences:
            sentence.bagOfWords = self.StemsBagOfWordsByPorter(sentence.bagOfWords)
        self._sentenceRepository.UpdateList(sentenceList.sentences)

    def StemsBagOfWordsByPorter(self, bagOfWords):
        stemmer = nltk.stem.porter.PorterStemmer()
        wordOccurenceDictionary = Counter()
        for word, occurence in bagOfWords.wordOccurenceDictionary.items():
            word = stemmer.stem(word)
            wordOccurenceDictionary.update({word: occurence})
        bagOfWords.wordOccurenceDictionary = wordOccurenceDictionary
        return bagOfWords
    #end_region [stem words in bag-of-words]
    
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
