
class PanFolderStructure():
    PAIRS_FILE_NAME = 'pairs'
    SOURCE_RAW_TEXTS_FOLDER = 'src'
    SUSPICIOUS_RAW_TEXT_FOLDER = 'susp'
    RANDOM_OBFUSCATION_DETECTION_FOLDER = '03-random-obfuscation'
    NO_OBFUSCATION_DETECTION_FOLDER = '02-no-obfuscation'
    NO_PLAGIARISM_DETECTION_FOLDER = '01-no-plagiarism'

class PanDetectionXmlStructure(): 
    class Document():
        class Attributes():
            REFERENCE = 'reference'
        class Feature():
            class Attributes():
                NAME = 'name'
                OBFUSCATION = 'obfuscation'
                OBFUSCATION_DEGREE = 'obfuscation_degree'
                SOURCE_LENGTH = 'source_length'
                SOURCE_OFFSET = 'source_offset'
                SOURCE_REFERENCE = 'source_reference'
                THIS_LENGTH = 'this_length'
                THIS_OFFSET = 'this_offset'
                TYPE = 'type'
            FEATURE = 'feature'
        DOCUMENT = 'document'

class PanDetectionXmlPlain():
    def __init__(self, name, obfuscation, obfuscationDegree, _type, suspiciousFileName,
        suspiciousLength, suspiciousOffset, sourceLength, sourceOffset, sourceFileName):
        self.name = name
        self.obfuscation = obfuscation
        self.obfuscationDegree = obfuscationDegree
        self._type = _type
        self.suspiciousFileName = suspiciousFileName
        self.suspiciousLength = suspiciousLength
        self.suspiciousOffset = suspiciousOffset
        self.sourceLength = sourceLength
        self.sourceOffset = sourceOffset
        self.sourceFileName = sourceFileName

