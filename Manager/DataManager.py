from Process import _DataImportationProcess as DataImportationProcess
from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose

class DataManager(object):

    def Hello(self):
        print ('Hello, I\'m the DataManager')
        print ('And I manage these processes:')
        self._dataImportationProcess.Hello()

    def ImportPanDataBase(self):
        trainTextCollectionMeta = TextCollectionMeta(
            sourceUrl = None,
            name = 'pan14-text-alignment-test-corpus3-2014-05-14_20180516_133851_p1_train',
            description = 'treino, base pan 2014-maio reduzida em 99%, amostragem aleatória',
            creationDate = '2014-05-14',
            purpose = TextCollectionMetaPurpose.train)
        trainFolderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan14-text-alignment-test-corpus3-2014-05-14_20180516_133851_p1_train\\'
        testTextCollectionMeta = TextCollectionMeta(
            sourceUrl = None,
            name = 'pan14-text-alignment-test-corpus3-2014-05-14_20180520_091948_p1_test',
            description = 'teste, base pan 2014-maio reduzida em 99%, amostragem aleatória',
            creationDate = '2014-05-14',
            purpose = TextCollectionMetaPurpose.test)
        testFolderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan14-text-alignment-test-corpus3-2014-05-14_20180520_091948_p1_test\\'        
        self._dataImportationProcess.ImportTrainTestDataFromPanFiles(
            testTextCollectionMeta = testTextCollectionMeta, 
            testFolderCompletePath = testFolderCompletePath, 
            trainTextCollectionMeta = trainTextCollectionMeta, 
            trainFolderCompletePath = trainFolderCompletePath)

    _dataImportationProcess = DataImportationProcess()

    def __init__(self):
        pass