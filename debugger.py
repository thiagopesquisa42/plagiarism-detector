#TODO: remove this 'debugger'
from Process import _PreProcessingRawTextProcess
from Repository import _RawTextRepository
from Entity import _RawText as RawText
import util

_PreProcessingRawTextProcess().PreProcessing(24)

# a = RawText(textCollectionMetaId = 24, text = "test insert functions heritage.", fileName = 'sem arquivo')
# _RawTextRepository().Insert(a)
# print(a.id)