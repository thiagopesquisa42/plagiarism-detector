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
            name = 'pan14-text-alignment-test-corpus3-2014-05-14_20180511_214100_p20',
            description = 'teste pan 2014-maio reduzida em 80%',
            creationDate = '2013-01-21')
        self._dataImportationProcess.ImportFromPanFiles(
            textCollectionMeta = textCollectionMeta, 
            folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan14-text-alignment-test-corpus3-2014-05-14_20180511_214100_p20\\')

    _dataImportationProcess = DataImportationProcess()

    def __init__(self):
        pass