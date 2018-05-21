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
            name = 'pan13-text-alignment-training-corpus-2013-01-21_20180520_235434_p1',
            description = 'treino, base pan 2013-jan reduzida em 99%, amostragem aleatória',
            creationDate = '2013-01-21',
            purpose = TextCollectionMetaPurpose.train)
        trainFolderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan13-text-alignment-training-corpus-2013-01-21_20180520_235434_p1\\'
        testTextCollectionMeta = TextCollectionMeta(
            sourceUrl = None,
            name = 'pan13-text-alignment-test-corpus2-2013-01-21_20180520_235355_p1',
            description = 'teste, base pan 2013-jan reduzida em 99%, amostragem aleatória',
            creationDate = '2013-01-21',
            purpose = TextCollectionMetaPurpose.test)
        testFolderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan13-text-alignment-test-corpus2-2013-01-21_20180520_235355_p1\\'        
        self._dataImportationProcess.ImportTrainTestDataFromPanFiles(
            testTextCollectionMeta = testTextCollectionMeta, 
            testFolderCompletePath = testFolderCompletePath, 
            trainTextCollectionMeta = trainTextCollectionMeta, 
            trainFolderCompletePath = trainFolderCompletePath)

    _dataImportationProcess = DataImportationProcess()

    def __init__(self):
        pass