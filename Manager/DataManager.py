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
            name = 'pan14-text-alignment-test-corpus3-2014-05-14_20180516_133851_p1',
            description = 'teste pan 2014-maio reduzida em 99%',
            creationDate = '2014-05-14')
        self._dataImportationProcess.ImportFromPanFiles(
            textCollectionMeta = textCollectionMeta, 
            folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan14-text-alignment-test-corpus3-2014-05-14_20180516_133851_p1\\')

    _dataImportationProcess = DataImportationProcess()

    def __init__(self):
        pass