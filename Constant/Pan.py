
PAIRS_FILE_NAME = 'pairs'
SOURCE_RAW_TEXTS_FOLDER = 'src'
SUSPICIOUS_RAW_TEXT_FOLDER = 'susp'
RANDOM_OBFUSCATION_DETECTION_FOLDER = '03-random-obfuscation'
NO_OBFUSCATION_DETECTION_FOLDER = '02-no-obfuscation'
NO_PLAGIARISM_DETECTION_FOLDER = '01-no-plagiarism'

def GetFeatureStructure():
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
    class Feature():
        FEATURE = 'feature'
        attributes = Attributes()
    return Feature()

def GetDocumentStructure():
    class Attributes():
        REFERENCE = 'reference'
    class Document():
        DOCUMENT = 'document'
        attributes = Attributes()
        featureChild = GetFeatureStructure()
    return Document()
class PanDetectionXmlStructure(object): 
    Structure = GetDocumentStructure()