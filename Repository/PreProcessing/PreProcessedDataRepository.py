from Repository import _BaseRepository as BaseRepository
from Entity.PreProcessing import _PreProcessedData as PreProcessedData

class PreProcessedDataRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(PreProcessedData).filter(PreProcessedData.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
