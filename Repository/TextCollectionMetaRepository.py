from Repository import _BaseRepository as BaseRepository

class TextCollectionMetaRepository(BaseRepository):
    def __init__(self, context):
        super().__init__(context, name = 'TextCollectionMeta')
