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
from Repository import _TextCollectionMetaRepository as TextCollectionMetaRepository
from Repository.PreProcessing import _PreProcessedDataRepository as PreProcessedDataRepository

class PreProcessingRawTextProcess(BaseProcess):

    def PreProcessing(self):
        try:
            self.logger.info('PreProcessing started')
            self.logger.info('Restoring Text Collection')
            textCollectionMeta = self._textCollectionMetaRepository.Get()
            self.logger.info('Creating Pre-processed-data instance')
            preProcessedData = self.CreatePreProcessedDataInstance(textCollectionMeta)
            
            self.logger.info('Tokenize in Sentences')
            preProcessedData = self.TokenizeRawTextInSentences(preProcessedData)
            preProcessedData = self._preProcessedDataRepository.StoreAndGet(preProcessedData)
            
            self.logger.info('To Lower')
            self.ToLowerSentenceListGroup(preProcessedData)
            preProcessedData = self._preProcessedDataRepository.StoreAndGet(preProcessedData)
            
            self.logger.info('Tokenize in Words, create Bag-of-Words')
            self.TokenizeSentenceListGroupInBagOfWords(preProcessedData)
            preProcessedData = self._preProcessedDataRepository.StoreAndGet(preProcessedData)
            
            self.logger.info('Remove stopwords from Bag-of-Words')
            self.RemoveStopWordsSentenceListGroup(preProcessedData)
            preProcessedData = self._preProcessedDataRepository.StoreAndGet(preProcessedData)

            self.logger.info('Fuse small sentences')
            self.SentenceListGroupInnerFusion(preProcessedData)
            preProcessedData = self._preProcessedDataRepository.StoreAndGet(preProcessedData)
            
            self.logger.info('Stem words from Bags-of-words')
            self.StemSentenceListGroup(preProcessedData)
            preProcessedData = self._preProcessedDataRepository.StoreAndGet(preProcessedData)
            
        except Exception as exception:
            self.logger.info('PreProcessing failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('PreProcessing finished')
            return preProcessedData

    def CreatePreProcessedDataInstance(self, textCollectionMeta):
        preProcessedData = PreProcessedData(textCollectionMeta = textCollectionMeta)
        return self._preProcessedDataRepository.StoreAndGet(preProcessedData)
    
    def AddPreProcessStepToStepChain(self, preProcessedData, preProcessStep):
        previousPreProcessStepChainNode = preProcessedData.topPreProcessStepChainNode
        preProcessStepChainNode = PreProcessStepChainNode(
            preProcessedData = preProcessedData,
            preProcessStep = preProcessStep,
            previousPreProcessStepChainNode = previousPreProcessStepChainNode,
            stepPosition = 0 if(previousPreProcessStepChainNode == None) else previousPreProcessStepChainNode.stepPosition + 1)
        preProcessedData.topPreProcessStepChainNode = preProcessStepChainNode
        return preProcessedData
    
    #region [Tokenize raw text in sentences]
    def TokenizeRawTextInSentences(self, preProcessedData):
        preProcessStep = self.CreateTokenizationStep(
            tokenizationType = TokenizationType.SENTENCE, 
            tokenizationAlgorithm = TokenizationAlgorithm.PUNKT_EN)
        preProcessedData = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        rawTextList = preProcessedData.textCollectionMeta.rawTextList
        preProcessedData.listOfSentenceList = self.CreateListOfSentenceListFromRawText(rawTextList)
        for sentenceList in preProcessedData.listOfSentenceList:
            sentenceList = self.CreateSentencesByPunktTokenizer(sentenceList)
        return preProcessedData

    def CreateTokenizationStep(self, tokenizationType, tokenizationAlgorithm, description = None):
        tokenization = Tokenization(
            _type = tokenizationType,
            algorithm = tokenizationAlgorithm, 
            description = description)
        preProcessStep = PreProcessStep(algorithm = tokenization.ToDictionary())
        return preProcessStep
    
    def CreateListOfSentenceListFromRawText(self, rawTextList):
        listOfSentenceList = []
        for rawText in rawTextList:
            sentenceList = SentenceList(rawText = rawText)
            listOfSentenceList.append(sentenceList)
        return listOfSentenceList

    def CreateSentencesByPunktTokenizer(self, sentenceList):
        sentenceDetector = nltk.data.load('tokenizers/punkt/english.pickle')
        rawText = sentenceList.rawText
        sentenceRawTextExcerptLocationList = [
            RawTextExcerptLocation(
                rawText = rawText,
                firstCharacterPosition = firstCharacterPosition,
                lastCharacterPosition = lastCharacterPosition,
                stringLength = lastCharacterPosition - firstCharacterPosition)
            for (firstCharacterPosition, lastCharacterPosition) in sentenceDetector.span_tokenize(rawText.text.decode())]
        sentenceTextList = sentenceDetector.tokenize(rawText.text.decode())
        sentences = []
        for index, text in enumerate(sentenceTextList):
            sentences.append(
                Sentence(
                    text = text,
                    rawTextExcerptLocation = sentenceRawTextExcerptLocationList[index]))
        sentenceList.sentences = sentences
        return sentenceList
    #end_region [Tokenize raw text in sentences]

    #region [To lower sentences]
    def ToLowerSentenceListGroup(self, preProcessedData):
        preProcessStep = self.CreateToLowerStep(description = 'em testes')
        preProcessedData = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        for sentenceList in preProcessedData.listOfSentenceList:
            sentenceList = self.ToLowerSentences(sentenceList)
        return preProcessedData

    def CreateToLowerStep(self, description = None):
        toLower = ToLower(description = description)
        preProcessStep = PreProcessStep(algorithm = toLower.ToDictionary())
        return preProcessStep

    def ToLowerSentences(self, sentenceList):
        for sentences in sentenceList.sentences:
            sentences.text = sentences.text.lower()
        return sentenceList
    #end_region [To lower sentences]

    #region [Tokenize in words]
    def TokenizeSentenceListGroupInBagOfWords(self, preProcessedData):
        preProcessStep = self.CreateTokenizationStep(
            tokenizationType = TokenizationType.WORD, 
            tokenizationAlgorithm = TokenizationAlgorithm.TREEBANK_WORD_TOKENIZER)
        preProcessedData = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        for sentenceList in preProcessedData.listOfSentenceList:
            sentenceList.sentences = self.TokenizeSentencesInBagOfWords(sentenceList.sentences)
        return preProcessedData

    def TokenizeSentencesInBagOfWords(self, sentences):
        sentences = self.CreateBagOfWordsByTreeBankWordTokenizer(sentences)
        return sentences

    def CreateBagOfWordsByTreeBankWordTokenizer(self, sentences):
        wordTokenizer = nltk.TreebankWordTokenizer()
        for sentence in sentences:
            wordsSimpleList = wordTokenizer.tokenize(sentence.text)
            wordOccurenceDictionary = Counter(wordsSimpleList)
            bagOfWords = BagOfWords(wordOccurenceDictionary = wordOccurenceDictionary)
            sentence.bagOfWords = bagOfWords
        return sentences
        
    #end_region [Tokenize in words]

    #region [Remove stopwords from bag-of-words]
    def RemoveStopWordsSentenceListGroup(self, preProcessedData):
        stopWordList = StopWord.STOP_WORD_FULL_LIST
        preProcessStep = self.CreateStopWordStep(
            stopWordList = stopWordList)
        preProcessedData = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        for sentenceList in preProcessedData.listOfSentenceList:
            sentenceList.sentences = self.RemoveStopWordsFromSentences(sentenceList.sentences, stopWordList)
        return preProcessedData

    def CreateStopWordStep(self, stopWordList, description = None):
        removeStopWords = RemoveStopWords(
            stopWordList = stopWordList, 
            description = description)
        preProcessStep = PreProcessStep(algorithm = removeStopWords.ToDictionary())
        return preProcessStep

    def RemoveStopWordsFromSentences(self, sentences, stopWordList):
        for sentence in sentences:
            sentence.bagOfWords = self.RemoveStopWordsFromBagOfWords(sentence.bagOfWords, stopWordList)
        return sentences

    def RemoveStopWordsFromBagOfWords(self, bagOfWords, stopWordList):
        bagOfWords.wordOccurenceDictionary = {
            word: occurence 
            for (word, occurence) in bagOfWords.wordOccurenceDictionary.items() 
            if word not in stopWordList}
        return bagOfWords
    #end_region [Remove stopwords from bag-of-words]

    #region [fuse sentences and bag-of-words]
    def SentenceListGroupInnerFusion(self, preProcessedData):
        threshold = Threshold.SENTENCE_NUMBER_WORDS_TO_FUSE
        preProcessStep = self.CreateFuseSentenceStep(threshold = threshold)
        preProcessedData = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        for sentenceList in preProcessedData.listOfSentenceList:
            sentenceList.sentences = self.SentencesInnerFusion(sentenceList.sentences, threshold)
        return preProcessedData

    def CreateFuseSentenceStep(self, threshold, description = None):
        fuseSentences = FuseSentences(
            threshold = threshold, 
            description = description)
        preProcessStep = PreProcessStep(algorithm = fuseSentences.ToDictionary())
        return preProcessStep

    def SortAscendentSentencesByLocation(self, sentences):
        return sorted(sentences, 
            key = lambda sentence: (sentence.rawTextExcerptLocation.firstCharacterPosition))

    def SentencesInnerFusion(self, sentences, threshold):
        if (len(sentences) == 0):
            return
        sortedSentences = self.SortAscendentSentencesByLocation(sentences)
        newSentences = []
        newSentences.append(sortedSentences[0])
        for sentence in sortedSentences[1:]:
            sentenceNumberWords = sum(sentence.bagOfWords.wordOccurenceDictionary.values())
            if( sentenceNumberWords <= threshold):
                newSentences = self.FuseWithLastSentence(newSentences, sentence)
            else:
                newSentences.append(sentence)
        return newSentences

    def FuseWithLastSentence(self, sentenceList, sentence):
        if (len(sentenceList) == 0):
            raise Exception('Error fusing sentence into empty list')
        sentenceDestination = sentenceList[-1] #get last item from list
        sentenceDestination.rawTextExcerptLocation.lastCharacterPosition =\
            sentence.rawTextExcerptLocation.lastCharacterPosition
        sentenceDestination.rawTextExcerptLocation.stringLength +=\
            sentence.rawTextExcerptLocation.stringLength
        sentenceDestination.text += ' ' + sentence.text
        sentenceDestination.bagOfWords = self.FuseBagOfWords(
            bagOfWordsDestination = sentenceDestination.bagOfWords,
            bagOfWords = sentence.bagOfWords)
        return sentenceList

    def FuseBagOfWords(self, bagOfWordsDestination, bagOfWords):
        destinationWordOccurenceDictionary = bagOfWordsDestination.wordOccurenceDictionary
        wordOccurenceDictionary = bagOfWords.wordOccurenceDictionary
        wordSimpleList = self.WordOccurenceDictionaryToWordList(
            destinationWordOccurenceDictionary)
        wordSimpleList.extend(self.WordOccurenceDictionaryToWordList(
            wordOccurenceDictionary))
        bagOfWordsDestination.wordOccurenceDictionary = Counter(wordSimpleList)
        return bagOfWordsDestination

    def WordOccurenceDictionaryToWordList(self, wordOccurenceDictionary):
        wordSimpleList = []
        for word, occurence in wordOccurenceDictionary.items():
            wordSimpleList.extend([word for index in range(0, occurence)])
        return wordSimpleList
    #end_region [fuse sentences and bag-of-words]

    #region [stem words in bag-of-words]
    def StemSentenceListGroup(self, preProcessedData):
        preProcessStep = self.CreateStemmerStep(stemmerAlgorithm = StemmerAlgorithm.PORTER)
        preProcessedData = self.AddPreProcessStepToStepChain(
            preProcessedData = preProcessedData, 
            preProcessStep = preProcessStep)
        for sentenceList in preProcessedData.listOfSentenceList:
            sentenceList.sentences = self.StemsSentencesByPorter(sentenceList.sentences)
        return preProcessedData

    def CreateStemmerStep(self, stemmerAlgorithm, description = None):
        stemmer = Stemmer(
            algorithm = stemmerAlgorithm, 
            description = description)
        preProcessStep = PreProcessStep(algorithm = stemmer.ToDictionary())
        return preProcessStep

    def StemsSentencesByPorter(self, sentences):
        for sentence in sentences:
            sentence.bagOfWords = self.StemsBagOfWordsByPorter(sentence.bagOfWords)
        return sentences

    def StemsBagOfWordsByPorter(self, bagOfWords):
        wordSimpleList = self.WordOccurenceDictionaryToWordList(
            bagOfWords.wordOccurenceDictionary)
        stemmer = nltk.stem.porter.PorterStemmer()
        wordSimpleList = [stemmer.stem(word) for word in wordSimpleList]
        bagOfWords.wordOccurenceDictionary = Counter(wordSimpleList)
        return bagOfWords
    #end_region [stem words in bag-of-words]


    def __init__(self):
        self._textCollectionMetaRepository = TextCollectionMetaRepository()
        self._preProcessedDataRepository = PreProcessedDataRepository()
        super().__init__()
