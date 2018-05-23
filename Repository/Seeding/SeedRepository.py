from Repository import _BaseRepository as BaseRepository
from Entity.Seeding import _Seed as Seed, _SeedingData as SeedingData

class SeedRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(Seed).filter(Seed.id == id).first()
    
    def GetListByRawTextPair(self, rawTextPair, seedingData):
        return self.session.query(Seed).\
            filter((Seed.rawTextPair == rawTextPair)\
                & (Seed.seedingData == seedingData)).all()

    #deprecated, too slow in big data
    def GetListBySeedingData(self, seedingData):
        return self.session.query(Seed).\
            filter(Seed.seedingData == seedingData).all()

    def GetRawListIdsBySeedingData(self, seedingData):
        rawListId = self.engine.execute(
            Seed.__table__.select(whereclause = "seedingDataId = " + str(seedingData.id))
        ).fetchall()
        return rawListId

    def InsertByRawSql(self, seedList):
        self.engine.execute(
            Seed.__table__.insert(),
            [seed.ToDictionary() for seed in seedList])

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
