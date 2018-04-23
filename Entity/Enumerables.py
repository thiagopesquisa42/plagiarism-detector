import enum

class RawTextType(enum.Enum):
    suspicious = 1000
    source = 2000

class PlagiarismObfuscation(enum.Enum):
    none = 1000

class PlagiarismType(enum.Enum):
    artificial = 1000

class EnumYesNo(enum.Enum):
    yes = 1000
    no = 2000
    