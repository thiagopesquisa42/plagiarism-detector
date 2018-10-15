import os
import enum

class LoggerConstant():
    class Name():
        REPOSITORY_SQLALCHEMY = 'sqlalchemy.engine'
        REPOSITORY = 'repository'
        INTERNAL = 'internal'
        PROCESS = 'process'
        MANAGER = 'manager'
        VIEW = 'view'

    class File():
        MAXIMUM_SIZE_MEGABYTES = 10
        FOLDER_PATH = 'log'
        BIG_LOG_FOLDER_PATH = os.path.join(FOLDER_PATH, 'big')
        FILE_EXTENSION = '.log'
        REPOSITORY_SQLALCHEMY = os.path.join(FOLDER_PATH, 'repository_sqlalchemy' + FILE_EXTENSION)
        REPOSITORY = os.path.join(FOLDER_PATH, 'repository' + FILE_EXTENSION)
        INTERNAL = os.path.join(FOLDER_PATH, 'internal' + FILE_EXTENSION)
        PROCESS = os.path.join(FOLDER_PATH, 'process' + FILE_EXTENSION)
        MANAGER = os.path.join(FOLDER_PATH, 'manager' + FILE_EXTENSION)
        VIEW = os.path.join(FOLDER_PATH, 'view' + FILE_EXTENSION)

class StopWord():
    STOP_WORD_50TH_LIST = [
        'the','of','and','a','in','to','is','was','it','for','with','he','be',
        'on','i','that','by','at','you','\'s','are','not','his','this','from',
        'but','had','which','she','they','or','an','were','we','their','been',
        'has','have','will','would','her','n\'t','there','can','all','as','if',
        'who','what','said']
    STOP_WORD_FULL_LIST = [
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
        'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
        'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
        'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
        'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
        'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 
        'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 
        'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
        'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', '\'s', 'n\'t', 'can',
        'will', 'just', 'don', 'should', 'now']

class Threshold():
    SENTENCE_NUMBER_WORDS_TO_FUSE = 3
    DETECTION_MINIMUM_PERCENTUAL_INTERSECTION = 0.5

class SeedAttributesNames():
    class Names():
        plagiarismClass = 'plagiarismClass'
        cosine = 'cosine'
        dice = 'dice'
        isMaxCosine = 'isMaxCosine'
        maxCosineDiff = 'maxCosineDiff'
        meanMaxCosineDiff = 'meanMaxCosineDiff'
        maxCosineNeighbour = 'maxCosineNeighbour'
        verticalCosineMaxDistance = 'verticalCosineMaxDistance'
        verticalCosineMaxMeasure = 'verticalCosineMaxMeasure'
        isMaxDice = 'isMaxDice'
        maxDiceDiff = 'maxDiceDiff'
        meanMaxDiceDiff = 'meanMaxDiceDiff'
        maxDiceNeighbour = 'maxDiceNeighbour'
        verticalDiceMaxDistance = 'verticalDiceMaxDistance'
        verticalDiceMaxMeasure = 'verticalDiceMaxMeasure'
        lengthRatio = 'lengthRatio'
        metaSeed = 'metaSeed'
        metaRawTextPair = 'metaRawTextPair'

    ATTRIBUTES = [
        Names.cosine,
        Names.dice,
        Names.isMaxCosine,
        Names.maxCosineDiff,
        Names.meanMaxCosineDiff,
        Names.maxCosineNeighbour,
        Names.verticalCosineMaxDistance,
        Names.verticalCosineMaxMeasure,
        Names.isMaxDice,
        Names.maxDiceDiff,
        Names.meanMaxDiceDiff,
        Names.maxDiceNeighbour,
        Names.verticalDiceMaxDistance,
        Names.verticalDiceMaxMeasure,
        Names.lengthRatio]
    
    REMOVE_LIST = [
        'percentualInDetection'
    ]

    TARGET_CLASS = Names.plagiarismClass

    META = [
        Names.metaSeed,
        Names.metaRawTextPair]

class PanFolders():
    ROOT = 'C:\\Users\\thiagopesquisa42\\Desktop\\panDatabases'
    FOLDER_2012 = os.path.join(ROOT, '2012')
    FOLDER_2013_TEST1_MARCH = os.path.join(ROOT, '2013-test1-march')
    FOLDER_2013_TEST2_JANUARY = os.path.join(ROOT, '2013-test2-january')
    FOLDER_2013_TRAIN_JANUARY = os.path.join(ROOT, '2013-train-january')
    FOLDER_2014 = os.path.join(ROOT, '2014')

class PanDataBaseLocation():
    class FullSamples():
        FOLDER_PATH_2013_TEST2_JANUARY = os.path.join(PanFolders.FOLDER_2013_TEST2_JANUARY, 'pan13-text-alignment-training-corpus-2013-01-21')
        FOLDER_PATH_2013_TRAIN_JANUARY = os.path.join(PanFolders.FOLDER_2013_TRAIN_JANUARY, 'pan13-text-alignment-test-corpus2-2013-01-21')

    class SubSampled():
        FOLDER_PATH_2013_TEST2_JANUARY_020_P = os.path.join(PanFolders.FOLDER_2013_TEST2_JANUARY, 'pan13-text-alignment-test-corpus2-2013-01-21_20180511_223813_p20')
        FOLDER_PATH_2013_TEST2_JANUARY_005_P = os.path.join(PanFolders.FOLDER_2013_TEST2_JANUARY, 'pan13-text-alignment-test-corpus2-2013-01-21_20180526_194019_p5')
        FOLDER_PATH_2013_TEST2_JANUARY_001_P = os.path.join(PanFolders.FOLDER_2013_TEST2_JANUARY, 'pan13-text-alignment-test-corpus2-2013-01-21_20180520_235355_p1')
        FOLDER_PATH_2013_TRAIN_JANUARY_020_P = os.path.join(PanFolders.FOLDER_2013_TRAIN_JANUARY, 'pan13-text-alignment-training-corpus-2013-01-21_20180511_223848_p20')
        FOLDER_PATH_2013_TRAIN_JANUARY_005_P = os.path.join(PanFolders.FOLDER_2013_TRAIN_JANUARY, 'pan13-text-alignment-training-corpus-2013-01-21_20180526_194057_p5')
        FOLDER_PATH_2013_TRAIN_JANUARY_001_P = os.path.join(PanFolders.FOLDER_2013_TRAIN_JANUARY, 'pan13-text-alignment-training-corpus-2013-01-21_20180520_235434_p1')
    
    fullSamples = FullSamples()
    subSampled = SubSampled()

class PanSettings():
    detectionName = 'detected-plagiarism'
    _type = 'artificial'

class SupportScripts():
    ROOT_FOLDER = 'support'
    FOLDER_PATH_PAN_OFFICIAL_METRIC_SCRIPT = os.path.join(ROOT_FOLDER, 'pan09-plagiarism-detection-performance-measures.py')

class ContextDefaultFolders():
    class Experiment():
        class Data():
            TRAINING_SUBFOLDER = 'train'
            TESTING_SUBFOLDER = 'test'
            CLASSIFIER_SUBFOLDER = 'classifier'
            META_SUBFOLDER = 'meta'
            PAN_FORMAT_DETECTIONS_SUBFOLDER = 'panDetections'
    ROOT_FOLDER = 'data'

class Contexts(enum.Enum):
    TRAIN = 1000
    TEST = 2000
    CLASSIFIER = 3000
    META = 4000
    PAN_FORMAT_DETECTIONS = 5000

class ClassifiersNickNames(enum.Enum):
    DECISION_TREE = 1000
    RANDOM_FOREST = 2000
    ADABOOST_DECISION_TREE = 3000