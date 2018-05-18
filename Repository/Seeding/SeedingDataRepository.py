from Repository import _BaseRepository as BaseRepository
from Entity.Seeding import _SeedingData as SeedingData

class SeedingDataRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(SeedingData).filter(SeedingData.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
