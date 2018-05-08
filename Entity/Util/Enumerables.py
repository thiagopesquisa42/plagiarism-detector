import enum

class RawTextType(enum.Enum):
    suspicious = 1000
    source = 2000
    
    @staticmethod
    def FromString(string):
        if(string == 'suspicious'):
            return RawTextType.suspicious
        if(string == 'source'):
            return RawTextType.source
        raise Exception('unknow RawTextType value')

class PlagiarismObfuscation(enum.Enum):
    none = 1000
    random = 2000

    @staticmethod
    def FromString(string):
        if(string == 'none'):
            return PlagiarismObfuscation.none
        if(string == 'random'):
            return PlagiarismObfuscation.random
        raise Exception('unknow PlagiarismObfuscation value')

class PlagiarismType(enum.Enum):
    artificial = 1000

    @staticmethod
    def FromString(string):
        if(string == 'artificial'):
            return PlagiarismType.artificial
        raise Exception('unknow PlagiarismType value')

class EnumYesNo(enum.Enum):
    yes = 1000
    no = 2000

    @staticmethod
    def FromBoolean(boolean):
        if(boolean is True):
            return EnumYesNo.yes
        if (boolean is False):
            return EnumYesNo.no
        raise Exception('unknow YesNo value')
    
class PreProcessName(enum.Enum):
    lower = 1000
    upper = 2000
    removeCharacterPunctuation = 3000
    stemming = 4000
    lemmatize = 5000
    tokenize = 6000
    nGram = 7000
    
    @staticmethod
    def FromString(string):
        if(string == 'lower'):
            return PreProcessName.lower
        if(string == 'upper'):
            return PreProcessName.upper
        if(string == 'removeCharacterPunctuation'):
            return PreProcessName.removeCharacterPunctuation
        if(string == 'stemming'):
            return PreProcessName.stemming
        if(string == 'lemmatize'):
            return PreProcessName.lemmatize
        if(string == 'tokenize'):
            return PreProcessName.tokenize
        if(string == 'nGram'):
            return PreProcessName.nGram
        raise Exception('unknow PreProcessName value')
    
class TokenizeType(enum.Enum):
    eachSpaceEndLine = 1000
    eachCharacter = 2000
    eachPunctuation = 3000
    
    @staticmethod
    def FromString(string):
        if(string == 'eachSpaceEndLine'):
            return TokenizeType.eachSpaceEndLine
        if(string == 'eachCharacter'):
            return TokenizeType.eachCharacter
        if(string == 'eachPunctuation'):
            return TokenizeType.eachPunctuation
        raise Exception('unknow TokenizeType value')

class StemmingType(enum.Enum):
    porter = 1000
    
    @staticmethod
    def FromString(string):
        if(string == 'porter'):
            return StemmingType.porter
        raise Exception('unknow StemmingType value')

class NGramType(enum.Enum):
    nGram = 1000
    nSkipGram = 2000
    
    @staticmethod
    def FromString(string):
        if(string == 'nGram'):
            return NGramType.nGram
        if(string == 'nSkipGram'):
            return NGramType.nSkipGram
        raise Exception('unknow NGramType value')

class BagType(enum.Enum):
    bagOfTexts = 1000
    bagOfSentences = 2000
    bagOfWords = 3000
    bagOfGramsSets = 4000
    
    @staticmethod
    def FromString(string):
        if(string == 'bagOfTexts'):
            return BagType.bagOfTexts
        if(string == 'bagOfSentences'):
            return BagType.bagOfSentences
        if(string == 'bagOfWords'):
            return BagType.bagOfWords
        if(string == 'bagOfGramsSets'):
            return BagType.bagOfGramsSets
        raise Exception('unknow BagType value')

