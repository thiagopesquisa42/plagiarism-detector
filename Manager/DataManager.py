from Process import _DataImportationProcess as DataImportationProcess
from Entity import _TextCollectionMeta as TextCollectionMeta

class DataManager(object):

    def Hello(self):
        print ('Hello, I\'m the DataManager')
        print ('And I manage these processes:')
        self._dataImportationProcess.Hello()

    def ImportPanDataBase(self):
        textCollectionMeta = TextCollectionMeta(
            sourceUrl = None,
            name = 'pan13-text-alignment-training-corpus-2013-01-21',
            description = 'teste pan 13-jan',
            creationDate = '2013-01-21')
        self._dataImportationProcess.ImportFromPanFiles(
            textCollectionMeta = textCollectionMeta, 
            folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan13-text-alignment-training-corpus-2013-01-21\\')

    _dataImportationProcess = DataImportationProcess()

    def __init__(self):
        pass