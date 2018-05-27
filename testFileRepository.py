import util
from Repository import _TextCollectionMetaRepository as TextCollectionMetaRepository
from Entity import _RawTextPair as RawTextPair
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Entity import _TextCollectionMeta as TextCollectionMeta
_textCollectionMetaRepository = TextCollectionMetaRepository()

tcm = TextCollectionMeta(
    creationDate = '2018-05-29',
    name = 'teste otimização em arquivo pickle',
    sourceUrl = 'sem url',
    description = 'teste',
    textCollectionMetaPurpose = TextCollectionMetaPurpose.train)

# _textCollectionMetaRepository.Store(tcm)
tcm = _textCollectionMetaRepository.Get()

print(str(tcm))


# tcm.rawTextPairList.append()