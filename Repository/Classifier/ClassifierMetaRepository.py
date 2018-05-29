from Repository import _BaseRepository as BaseRepository
import os

class ClassifierMetaRepository(BaseRepository):
    name = 'ClassifierMeta'

    def __init__(self):
        self.subFolder = 'classifier'
        super().__init__()
