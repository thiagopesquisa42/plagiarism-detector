import util
#TODO: remove this 'debugger'
from Process import _PreProcessingRawTextProcess
from Repository import _RawTextRepository
from Entity import _RawText as RawText

_PreProcessingRawTextProcess().PreProcessing(24)

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
