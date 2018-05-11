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
