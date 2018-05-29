import util
from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Process import _DataImportationProcess as DataImportationProcess
from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess
from Process import _SeedingProcess as SeedingProcess
from Process import _SeedingDataProcess as SeedingDataProcess
from Process import _SeedingClassifierProcess as SeedingClassifierProcess
import settings
import os

def CommomProcessing():
    _preProcessingRawTextProcess = PreProcessingRawTextProcess()
    preProcessedData = _preProcessingRawTextProcess.PreProcessing()
    print('finished')

    _seedingProcess = SeedingProcess()
    preProcessedData = _seedingProcess.SeedingProcessing()
    print('finished')

    _seedingDataProcess = SeedingDataProcess()
    dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingData()
    print('finished')

def GetLastFolderName(folderPath = ''):
    path, folder = os.path.split(folderPath)
    if(folder == ''):
        path, folder = os.path.split(path)
    return folder

settings.SetRootLocation('experiment01')
settings.SetCurrentSubFolder('train')

_dataImportationProcess = DataImportationProcess()

trainFolderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\panDatabases\\2013-train-january\\pan13-text-alignment-training-corpus-2013-01-21_20180520_235434_p1'
trainTextCollectionMeta = TextCollectionMeta(
    sourceUrl = None,
    name = GetLastFolderName(trainFolderCompletePath),
    description = 'treino, base pan 2013-jan 01%',
    creationDate = '2013-01-21',
    textCollectionMetaPurpose = TextCollectionMetaPurpose.train)
trainTextCollectionMeta = _dataImportationProcess.ImportFromPanFiles(
    textCollectionMeta = trainTextCollectionMeta, 
    folderCompletePath = trainFolderCompletePath)
print('finished')

CommomProcessing()

settings.SetCurrentSubFolder('test')
_dataImportationProcess = DataImportationProcess()

testFolderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\panDatabases\\2013-test2-january\\pan13-text-alignment-test-corpus2-2013-01-21_20180520_235355_p1'
testTextCollectionMeta = TextCollectionMeta(
    sourceUrl = None,
    name = GetLastFolderName(testFolderCompletePath),
    description = 'teste, base pan 2013-jan 01%',
    creationDate = '2013-01-21',
    textCollectionMetaPurpose = TextCollectionMetaPurpose.test)
testTextCollectionMeta = _dataImportationProcess.ImportFromPanFiles(
    textCollectionMeta = testTextCollectionMeta, 
    folderCompletePath = testFolderCompletePath)
print('finished')

CommomProcessing()

settings.SetCurrentSubFolder('train')
_seedingClassifierProcess = SeedingClassifierProcess()
classifierMetaTrained = _seedingClassifierProcess.TrainSeedClassifier()
print('finished')

settings.SetCurrentSubFolder('test')
_seedingClassifierProcess = SeedingClassifierProcess()
classifierMetaTested = _seedingClassifierProcess.TestSeedClassifier()
print('finished')