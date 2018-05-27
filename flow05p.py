import util
from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Process import _DataImportationProcess as DataImportationProcess
from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess
from Process import _SeedingProcess as SeedingProcess
import os
import pickle
import inspect
_thisModuleName = 'flow05p'
_dataImportationProcess = DataImportationProcess()
_seedingProcess = SeedingProcess()
_preProcessingRawTextProcess = PreProcessingRawTextProcess()

def ReduceTrainTestPanDataBase():
    panTest05pFolderCompletePath = _dataImportationProcess.DecreasePanDataBaseInNewFolder(
        decreasePercentage = 0.95,
        folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\panDatabases\\2013-test2-january\\pan13-text-alignment-test-corpus2-2013-01-21\\')
    panTrain05pFolderCompletePath = _dataImportationProcess.DecreasePanDataBaseInNewFolder(
        decreasePercentage = 0.95,
        folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\panDatabases\\2013-train-january\\pan13-text-alignment-training-corpus-2013-01-21\\')
    return panTrain05pFolderCompletePath, panTest05pFolderCompletePath

def GetLastFolderName(folderPath = ''):
    path, folder = os.path.split(folderPath)
    if(folder == ''):
        path, folder = os.path.split(path)
    return folder

def ImportTrainTestPanDataBase(trainFolderCompletePath, testFolderCompletePath):
    trainTextCollectionMeta = TextCollectionMeta(
        sourceUrl = None,
        name = GetLastFolderName(trainFolderCompletePath),
        description = 'treino, base pan 2013-jan reduzida em 95%, amostragem aleatória',
        creationDate = '2013-01-21',
        purpose = TextCollectionMetaPurpose.train)
    testTextCollectionMeta = TextCollectionMeta(
        sourceUrl = None,
        name = GetLastFolderName(testFolderCompletePath),
        description = 'teste, base pan 2013-jan reduzida em 95%, amostragem aleatória',
        creationDate = '2013-01-21',
        purpose = TextCollectionMetaPurpose.test)
    trainTextCollectionMeta, testTextCollectionMeta = _dataImportationProcess.\
        ImportTrainTestDataFromPanFiles(
            testTextCollectionMeta = testTextCollectionMeta, 
            testFolderCompletePath = testFolderCompletePath, 
            trainTextCollectionMeta = trainTextCollectionMeta, 
            trainFolderCompletePath = trainFolderCompletePath)
    return trainTextCollectionMeta.id, testTextCollectionMeta.id
    
def GetPickleFileReader():
    pickleName = _thisModuleName + '.pickle'
    return open(pickleName, 'rb')
def GetPickleFileWriter():
    pickleName = _thisModuleName + '.pickle'
    return open(pickleName, 'wb')

# tupleTrainTestFolders = ReduceTrainTestPanDataBase()
# pickle.dump(tupleTrainTestFolders, GetPickleFileWriter())
# tupleTrainTestFolders = pickle.load(GetPickleFileReader())

# tupleTrainTestTextCollectionMetaIds = ImportTrainTestPanDataBase(
#     trainFolderCompletePath = tupleTrainTestFolders[0],
#     testFolderCompletePath = tupleTrainTestFolders[1])
# pickle.dump(tupleTrainTestTextCollectionMetaIds, GetPickleFileWriter())
# tupleTrainTestTextCollectionMetaIds = pickle.load(GetPickleFileReader())

# preProcessedDataTrain = _preProcessingRawTextProcess.PreProcessing(
#      textCollectionMetaId = tupleTrainTestTextCollectionMetaIds[0])
# preProcessedDataTest = _preProcessingRawTextProcess.PreProcessing(
#     textCollectionMetaId = tupleTrainTestTextCollectionMetaIds[1])

# tupleTrainTestPreProcessedDataIds = preProcessedDataTrain.id, preProcessedDataTest.id
# pickle.dump(tupleTrainTestPreProcessedDataIds, GetPickleFileWriter())
tupleTrainTestPreProcessedDataIds = pickle.load(GetPickleFileReader())

# seedingDataTrain = _seedingProcess.SeedingProcessing(preProcessedDataId = tupleTrainTestPreProcessedDataIds[0])
seedingDataTest = _seedingProcess.SeedingProcessing(preProcessedDataId = tupleTrainTestPreProcessedDataIds[1])

tupleTrainTestSeedingDataIds = seedingDataTrain.id, seedingDataTest.id
pickle.dump(tupleTrainTestSeedingDataIds, GetPickleFileWriter())
tupleTrainTestSeedingDataIds = pickle.load(GetPickleFileReader())
    

