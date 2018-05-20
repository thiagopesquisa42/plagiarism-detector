from Repository import _BaseRepository as BaseRepository
from Entity.Classifier import _SeedingDataFrame as SeedingDataFrame

class SeedingDataFrameRepository(BaseRepository):
    def Get(self, id):
        return self.session.query(SeedingDataFrame).filter(SeedingDataFrame.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
