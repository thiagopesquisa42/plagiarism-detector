import util
from constant import PanDataBaseLocation
from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Process import _DataImportationProcess as DataImportationProcess
from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess
from Process import _SeedingProcess as SeedingProcess
from Process import _SeedingDataProcess as SeedingDataProcess
from Process import _SeedingClassifierProcess as SeedingClassifierProcess
import settings
import os

def SetExperimentName(experimentName):
    settings.SetRootLocation(experimentName)

def SetNewExperimentName(experimentName):
    SetExperimentName(experimentName)
    if(os.path.exists(settings.rootLocation)):
        raise Exception('There are a experiment with same name already.')

def ProcessTrainData():
    settings.SetCurrentSubFolder(settings.TRAINING_SUBFOLDER)
    _dataImportationProcess = DataImportationProcess()
    trainFolderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TRAIN_JANUARY_001_P
    trainTextCollectionMeta = TextCollectionMeta(
        sourceUrl = None,
        name = GetLastFolderName(trainFolderCompletePath),
        description = 'treino, base pan 2013-jan 001%',
        creationDate = '2013-01-21',
        textCollectionMetaPurpose = TextCollectionMetaPurpose.train)
    trainTextCollectionMeta = _dataImportationProcess.ImportFromPanFiles(
        textCollectionMeta = trainTextCollectionMeta, 
        folderCompletePath = trainFolderCompletePath)
    CommomProcessing()

def ProcessTestData():
    settings.SetCurrentSubFolder(settings.TESTING_SUBFOLDER)
    _dataImportationProcess = DataImportationProcess()
    testFolderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TEST2_JANUARY_001_P
    testTextCollectionMeta = TextCollectionMeta(
        sourceUrl = None,
        name = GetLastFolderName(testFolderCompletePath),
        description = 'teste, base pan 2013-jan 001%',
        creationDate = '2013-01-21',
        textCollectionMetaPurpose = TextCollectionMetaPurpose.test)
    testTextCollectionMeta = _dataImportationProcess.ImportFromPanFiles(
        textCollectionMeta = testTextCollectionMeta, 
        folderCompletePath = testFolderCompletePath)
    CommomProcessing()

def GetLastFolderName(folderPath = ''):
    path, folder = os.path.split(folderPath)
    if(folder == ''):
        path, folder = os.path.split(path)
    return folder

def CommomProcessing():
    _preProcessingRawTextProcess = PreProcessingRawTextProcess()
    preProcessedData = _preProcessingRawTextProcess.PreProcessing()
    _seedingProcess = SeedingProcess()
    preProcessedData = _seedingProcess.SeedingProcessing()
    _seedingDataProcess = SeedingDataProcess()
    dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingData()

def TrainingClassifier():
    settings.SetCurrentSubFolder(settings.TRAINING_SUBFOLDER)
    _seedingClassifierProcess = SeedingClassifierProcess()
    classifierMetaTrained = _seedingClassifierProcess.TrainSeedClassifier()

def TestingClassifier():
    settings.SetCurrentSubFolder(settings.TESTING_SUBFOLDER)
    _seedingClassifierProcess = SeedingClassifierProcess()
    classifierMetaTested = _seedingClassifierProcess.TestSeedClassifier()

experimentName = 'experiment005p_tape001'
# SetNewExperimentName(experimentName)
SetExperimentName(experimentName)
ProcessTrainData()
ProcessTestData()
TestingClassifier()
TrainingClassifier()