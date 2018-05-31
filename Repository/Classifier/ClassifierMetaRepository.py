from Repository import _BaseRepository as BaseRepository
from constant import Contexts

class ClassifierMetaRepository(BaseRepository):
    def __init__(self):
        super().__init__(context = Contexts.CLASSIFIER, name = 'ClassifierMeta')
