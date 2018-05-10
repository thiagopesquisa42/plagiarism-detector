from Repository import _BaseRepository as BaseRepository
from Entity import _RawTextPair as RawTextPair

class RawTextPairRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(RawTextPair).filter(RawTextPair.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
