import os

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

class TextCollectionMeta():
    ID_ONE_PERCENT_PAN_2014_TRAIN = 1
    ID_ONE_PERCENT_PAN_2014_TEST = 2

class PreProcessedData():
    ID_CURRENT = 1

class SeedingData():
    class TestTrainPair():
        CURRENT_TEST_ID = None
        CURRENT_TRAIN_ID = 1
    IDS = TestTrainPair

class SeedAttributesNames():
    class Names():
        seedId = 'seedId'
        plagiarismClass = 'plagiarismClass'
        percentualInDetection = 'percentualInDetection'
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

    ATTRIBUTES = [
        Names.seedId,
        Names.plagiarismClass,
        Names.percentualInDetection,
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
        Names.seedId,
        Names.percentualInDetection]

