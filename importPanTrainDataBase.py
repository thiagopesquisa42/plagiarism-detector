import util
from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Process import _DataImportationProcess as DataImportationProcess
import os

_dataImportationProcess = DataImportationProcess()


def GetLastFolderName(folderPath = ''):
    path, folder = os.path.split(folderPath)
    if(folder == ''):
        path, folder = os.path.split(path)
    return folder

trainFolderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\panDatabases\\2013-train-january\\pan13-text-alignment-training-corpus-2013-01-21_20180520_235434_p1'
trainTextCollectionMeta = TextCollectionMeta(
    sourceUrl = None,
    name = GetLastFolderName(trainFolderCompletePath),
    description = 'treino, base pan 2013-jan reduzida em 95%, amostragem aleatória',
    creationDate = '2013-01-21',
    textCollectionMetaPurpose = TextCollectionMetaPurpose.train)
trainTextCollectionMeta = _dataImportationProcess.ImportFromPanFiles(
    textCollectionMeta = trainTextCollectionMeta, 
    folderCompletePath = trainFolderCompletePath)
print('finished')