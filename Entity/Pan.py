
class PanFolderStructure():
    PAIRS_FILE_NAME = 'pairs'
    SOURCE_RAW_TEXTS_FOLDER = 'src'
    SUSPICIOUS_RAW_TEXT_FOLDER = 'susp'
    
    NO_PLAGIARISM_DETECTION_FOLDER = '01-no-plagiarism'
    NO_OBFUSCATION_DETECTION_FOLDER = '02-no-obfuscation'
    RANDOM_OBFUSCATION_DETECTION_FOLDER = '03-random-obfuscation'
    TRANSLATION_OBFUSCATION_DETECTION_FOLDER = '04-translation-obfuscation'
    SUMMARY_OBFUSCATION_DETECTION_FOLDER = '05-summary-obfuscation'
    NO_PLAGIARISM_DETECTION_FOLDER_PAN12 = '01_no_plagiarism'
    NO_OBFUSCATION_DETECTION_FOLDER_PAN12 = '02_no_obfuscation'
    ARTIFICIAL_LOW_OBFUSCATION_DETECTION_FOLDER = '03_artificial_low'
    ARTIFICIAL_HIGH_OBFUSCATION_DETECTION_FOLDER = '04_artificial_high'
    TRANSLATION_OBFUSCATION_DETECTION_FOLDER_PAN12 = '05_translation'
    SIMULATED_OBFUSCATION_DETECTION_FOLDER = '06_simulated_paraphrase'
    DETECTION_FOLDER_NAME_LIST = [
        NO_PLAGIARISM_DETECTION_FOLDER,
        # NO_OBFUSCATION_DETECTION_FOLDER,
        # RANDOM_OBFUSCATION_DETECTION_FOLDER,
        TRANSLATION_OBFUSCATION_DETECTION_FOLDER,
        SUMMARY_OBFUSCATION_DETECTION_FOLDER,
        NO_PLAGIARISM_DETECTION_FOLDER_PAN12,
        NO_OBFUSCATION_DETECTION_FOLDER_PAN12,
        ARTIFICIAL_LOW_OBFUSCATION_DETECTION_FOLDER,
        ARTIFICIAL_HIGH_OBFUSCATION_DETECTION_FOLDER,
        TRANSLATION_OBFUSCATION_DETECTION_FOLDER_PAN12,
        SIMULATED_OBFUSCATION_DETECTION_FOLDER]


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

