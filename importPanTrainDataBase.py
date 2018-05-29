import util
from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Process import _DataImportationProcess as DataImportationProcess
import os

# _dataImportationProcess = DataImportationProcess()


# def GetLastFolderName(folderPath = ''):
#     path, folder = os.path.split(folderPath)
#     if(folder == ''):
#         path, folder = os.path.split(path)
#     return folder

# trainFolderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\panDatabases\\2013-test2-january\\pan13-text-alignment-test-corpus2-2013-01-21_20180526_194019_p5'
# trainTextCollectionMeta = TextCollectionMeta(
#     sourceUrl = None,
#     name = GetLastFolderName(trainFolderCompletePath),
#     description = 'teste, base pan 2013-jan 05%',
#     creationDate = '2013-01-21',
#     textCollectionMetaPurpose = TextCollectionMetaPurpose.test)
# trainTextCollectionMeta = _dataImportationProcess.ImportFromPanFiles(
#     textCollectionMeta = trainTextCollectionMeta, 
#     folderCompletePath = trainFolderCompletePath)
# print('finished')

# from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess

# _preProcessingRawTextProcess = PreProcessingRawTextProcess()
# preProcessedData = _preProcessingRawTextProcess.PreProcessing()
# print('finished')


# from Process import _SeedingProcess as SeedingProcess

# _seedingProcess = SeedingProcess()
# preProcessedData = _seedingProcess.SeedingProcessing()
# print('finished')

# from Process import _SeedingDataProcess as SeedingDataProcess

# _seedingDataProcess = SeedingDataProcess()
# dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingData()
# print('finished')

from Process import _SeedingClassifierProcess as SeedingClassifierProcess

_seedingClassifierProcess = SeedingClassifierProcess()
# classifierMetaTrained = _seedingClassifierProcess.TrainSeedClassifier()
classifierMetaTested = _seedingClassifierProcess.TestSeedClassifier()
print('finished')