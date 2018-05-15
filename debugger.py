#TODO: remove this 'debugger'
import util
from Process import _PreProcessingRawTextProcess
from Repository import _RawTextRepository
from Entity import _RawText as RawText

_PreProcessingRawTextProcess().PreProcessing(textCollectionMetaId = 32)

# a = RawText(textCollectionMetaId = 24, text = "test insert functions heritage.", fileName = 'sem arquivo')
# _RawTextRepository().Insert(a)
# print(a.id)

# from Entity.PreProcessing import _PreProcessStep
# from Entity.PreProcessing.Algorithm import _Tokenization
# from Entity.PreProcessing.Algorithm import _TokenizationAlgorithm
# from Entity.PreProcessing.Algorithm import _TokenizationType
# from Repository.PreProcessing import _PreProcessStepRepository

# algorithm = _Tokenization(
#     _type = _TokenizationType.SENTENCE,
#     algorithm = _TokenizationAlgorithm.PUNKT_EN,
#     description='teste'
# )
# step = _PreProcessStep(algorithm = algorithm)
# #step = _PreProcessStep(algorithm = algorithm.ToDictionary())

# _PreProcessStepRepository().Insert(step)

# from Process import _DataImportationProcess
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.8,
    # folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan14-text-alignment-test-corpus3-2014-05-14\\')
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.8,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan13-text-alignment-test-corpus1-2013-03-08\\')
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.8,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan13-text-alignment-test-corpus2-2013-01-21\\')
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.8,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan13-text-alignment-training-corpus-2013-01-21\\')
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.8,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan12-text-alignment-training-corpus-2012-03-16\\') #-> failed, 2012 doesn't have pair file in the root!!
# _DataImportationProcess().DecreasePanDataBaseInNewFolder(
#     decreasePercentage = 0.95,
#     folderCompletePath = 'C:\\Users\\thiagopesquisa42\\Desktop\\pan14-text-alignment-test-corpus3-2014-05-14\\')
