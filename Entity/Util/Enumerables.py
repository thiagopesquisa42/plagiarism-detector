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
    translation = 3000
    summary = 4000

    @staticmethod
    def FromString(string):
        if(string == 'none'):
            return PlagiarismObfuscation.none
        if(string == 'random'):
            return PlagiarismObfuscation.random
        if(string == 'translation'):
            return PlagiarismObfuscation.random
        if(string == 'summary'):
            return PlagiarismObfuscation.random
        raise Exception('unknow PlagiarismObfuscation value')

class PlagiarismType(enum.Enum):
    artificial = 1000

    @staticmethod
    def FromString(string):
        if(string == 'artificial'):
            return PlagiarismType.artificial
        raise Exception('unknow PlagiarismType value')

class PlagiarismClass(enum.Enum):
    none = 1000
    direct = 2000
    obfuscatedRandom = 3000
    obfuscatedTranslation = 4000
    obfuscatedSummary = 5000

    @staticmethod
    def FromPlagiarismObfuscation(plagiarismObfuscation):
        if(plagiarismObfuscation == PlagiarismObfuscation.none):
            return PlagiarismClass.direct
        if(plagiarismObfuscation == PlagiarismObfuscation.random):
            return PlagiarismClass.obfuscatedRandom
        if(plagiarismObfuscation == PlagiarismObfuscation.summary):
            return PlagiarismClass.obfuscatedSummary
        if(plagiarismObfuscation == PlagiarismObfuscation.translation):
            return PlagiarismClass.obfuscatedTranslation
        raise Exception('impossible cast this PlagiarismObfuscation to PlagiarismClass')

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
