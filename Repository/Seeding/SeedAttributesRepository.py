from Repository import _BaseRepository as BaseRepository
from Entity.Seeding import _SeedAttributes as SeedAttributes
from Entity.Seeding import _SeedingData as SeedingData
from Entity.Seeding import _Seed as Seed

class SeedAttributesRepository(BaseRepository):
    def Get(self, seed):
        return self.session.query(SeedAttributes).filter(SeedAttributes.seed == seed).first()

    def GetListBySeedingData(self, seedingData):
        return self.session.query(
            SeedAttributes).join(
                Seed).filter(
                    Seed.seedingData == seedingData).all()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
