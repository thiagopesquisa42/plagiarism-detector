from Util import _LoggerUtil as LoggerUtil
from Util import _ContextManager as ContextManager
from constant import PanDataBaseLocation, Contexts
from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Process import _DataImportationProcess as DataImportationProcess
from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess
from Process import _SeedingProcess as SeedingProcess
from Process import _SeedingDataProcess as SeedingDataProcess
from Process import _SeedingClassifierProcess as SeedingClassifierProcess
import os

def ProcessTrainData():
    ImportTrainDataBase()
    CommomProcessing(context = Contexts.TRAIN)

def ProcessTestData():
    ImportTestDataBase()
    CommomProcessing(context = Contexts.TEST)

def ImportTrainDataBase():
    _dataImportationProcess = DataImportationProcess(context = Contexts.TRAIN)
    trainTextCollectionMeta = _dataImportationProcess.ImportTrainDataBaseFromPanFiles(
        folderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TRAIN_JANUARY_005_P, 
        description = 'treino, base pan 2013-jan 005%',
        originalCreationDate = '2013-01-21')

def ImportTestDataBase():
    _dataImportationProcess = DataImportationProcess(context = Contexts.TEST)
    testTextCollectionMeta = _dataImportationProcess.ImportTrainDataBaseFromPanFiles(
        folderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TEST2_JANUARY_005_P, 
        description = 'teste, base pan 2013-jan 005%',
        originalCreationDate = '2013-01-21')

def CommomProcessing(context):
    _preProcessingRawTextProcess = PreProcessingRawTextProcess(context = context)
    preProcessedData = _preProcessingRawTextProcess.PreProcessing()
    _seedingProcess = SeedingProcess(context = context)
    preProcessedData = _seedingProcess.SeedingProcessing()
    _seedingDataProcess = SeedingDataProcess(context = context)
    dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingData()

def CreateSummaryDrivenDataFrame():
    _seedingDataProcess = SeedingDataProcess(context = Contexts.TRAIN)
    dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingDataSummaryDriven()
    _seedingDataProcess = SeedingDataProcess(context = Contexts.TEST)
    dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingDataSummaryDriven()

def TrainingClassifier():
    _seedingClassifierProcess = SeedingClassifierProcess()
    classifierMetaTrained = _seedingClassifierProcess.TrainSeedClassifier()

def TestingClassifier():
    _seedingClassifierProcess = SeedingClassifierProcess()
    classifierMetaTested = _seedingClassifierProcess.TestSeedClassifier()

def Main():
    # experimentName = 'experiment005p_tape003_summary'
    # experimentName = 'experiment005p_tape002'
    experimentName = 'experiment005p_tape001'
    # ContextManager.InitExperiment(experimentUniqueName = experimentName)
    ContextManager.ContinueExperiment(experimentUniqueName = experimentName)
    # CreateSummaryDrivenDatFrame()
    # ProcessTrainData()
    ProcessTestData()
    TrainingClassifier()
    TestingClassifier()

Main()