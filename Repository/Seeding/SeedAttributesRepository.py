from Repository import _BaseRepository as BaseRepository
from Repository.Seeding import _SeedRepository as SeedRepository
from Entity.Seeding import _SeedAttributes as SeedAttributes
from Entity.Seeding import _SeedingData as SeedingData
from Entity.Seeding import _Seed as Seed

class SeedAttributesRepository(BaseRepository):
    def Get(self, seed):
        return self.session.query(SeedAttributes).filter(SeedAttributes.seed == seed).first()

    def GetListBySeedingData(self, seedingData):
        seedList = self._seedRepository.GetListBySeedingData(seedingData)
        seedAttributesList = [seed.attributes for seed in seedList]
        return seedAttributesList

    def Hello(self):
        print ('Hello, I\'m a repository')

    _seedRepository = SeedRepository()

    def __init__(self):
        super().__init__()
