from Repository import _BaseRepository as BaseRepository
import settings
import os

class TextCollectionMetaRepository(BaseRepository):
    name = 'TextCollectionMeta'

    def __init__(self):
        self.subFolder = settings.currentSubFolder
        super().__init__()
