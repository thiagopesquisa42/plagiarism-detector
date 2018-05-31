from Repository import _BaseRepository as BaseRepository
from Entity.PreProcessing.TextStructure import _BagOfWords as BagOfWords

class BagOfWordsRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(BagOfWords).filter(BagOfWords.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
