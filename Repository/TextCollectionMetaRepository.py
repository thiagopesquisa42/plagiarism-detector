from Repository import _BaseRepository as BaseRepository
import os

class TextCollectionMetaRepository(BaseRepository):
    name = 'TextCollectionMetaRepository'

    def __init__(self):
        super().__init__()
        rootLocation = os.path.join(self.rootLocation, self.name)
