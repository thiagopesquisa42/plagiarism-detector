#TODO: remove this 'debugger'
import util
from Process import _PreProcessingRawTextProcess
from Process import _SeedingProcess, _SeedingClassifierProcess, _SeedingDataProcess
from Repository import _RawTextRepository
from Repository.Seeding import _SeedingDataRepository
from Repository.Classifier import _SeedingDataFrameRepository
from Entity import _RawText as RawText, _TextCollectionMetaPurpose
from constant import TextCollectionMeta, PreProcessedData, SeedingData

# preProcessedData = _PreProcessingRawTextProcess().PreProcessing(
#      textCollectionMetaId = TextCollectionMeta.ID_ONE_PERCENT_PAN_2013_TRAIN)
# preProcessedDataTest = _PreProcessingRawTextProcess().PreProcessing(
#     textCollectionMetaId = TextCollectionMeta.ID_ONE_PERCENT_PAN_2013_TEST)

# seedingData = _SeedingProcess().SeedingProcessing(preProcessedDataId = preProcessedData.id)
# seedingDataTest = _SeedingProcess().SeedingProcessing(preProcessedDataId = preProcessedDataTest.id)

# seedingDataFrame = _SeedingDataProcess().CreateSeedingDataFrameFromSeedingData(
#     seedingDataId = 2, textCollectionMetaPurpose = _TextCollectionMetaPurpose.train)
# seedingDataFrameTest = _SeedingDataProcess().CreateSeedingDataFrameFromSeedingData(
#     seedingDataId = 4, textCollectionMetaPurpose =_TextCollectionMetaPurpose.test)

_seedingDataFrameRepository = _SeedingDataFrameRepository()
seedingDataFrameTrain = _SeedingDataProcess().AlterSeedingData(seedingDataFrame = _seedingDataFrameRepository.Get(id = 8))
seedingDataFrameTest = _SeedingDataProcess().AlterSeedingData(seedingDataFrame = _seedingDataFrameRepository.Get(id = 9))

classifierMeta = _SeedingClassifierProcess().TrainSeedClassifier(seedingDataFrame = seedingDataFrameTrain)
classifierMetaTest = _SeedingClassifierProcess().TestSeedClassifier(seedingDataFrame = seedingDataFrameTest, classifierMeta = classifierMeta)





# from Process import _DataImportationProcess
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.8,
    # folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan14-text-alignment-test-corpus3-2014-05-14\\')
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.8,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan13-text-alignment-test-corpus1-2013-03-08\\')
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.99,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan13-text-alignment-test-corpus2-2013-01-21\\')
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.99,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan13-text-alignment-training-corpus-2013-01-21\\')
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.8,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan12-text-alignment-training-corpus-2012-03-16\\') #-> failed, 2012 doesn't have pair file in the root!!
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.95,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan14-text-alignment-test-corpus3-2014-05-14\\')
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.99,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan14-text-alignment-test-corpus3-2014-05-14\\')
