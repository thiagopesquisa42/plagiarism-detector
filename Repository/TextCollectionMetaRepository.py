from Repository import _BaseRepository as BaseRepository
from Entity import _TextCollectionMeta as TextCollectionMeta

class TextCollectionMetaRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(TextCollectionMeta).filter(TextCollectionMeta.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
