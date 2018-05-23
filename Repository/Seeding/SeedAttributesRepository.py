from Repository import _BaseRepository as BaseRepository
from Repository.Seeding import _SeedRepository as SeedRepository
from Entity.Seeding import _SeedAttributes as SeedAttributes
from Entity.Seeding import _SeedingData as SeedingData
from Entity.Seeding import _Seed as Seed
from sqlalchemy.sql import select

class SeedAttributesRepository(BaseRepository):
    def Get(self, seed):
        return self.session.query(SeedAttributes).filter(SeedAttributes.seed == seed).first()

    #deprecated, too slow in big data
    def GetListBySeedingData(self, seedingData):
        seedList = self._seedRepository.GetListBySeedingData(seedingData)
        seedAttributesList = [seed.attributes for seed in seedList]
        return seedAttributesList

    def GetRawListAllFieldsBySeedingData(self, seedingData):
        columns = SeedAttributes.GetColumnList()
        columnsNames = [column.name for column in columns]
        query = select(columnsNames)
        query = query.where("seedingDataId = " + str(seedingData.id))
        query = query.select_from('seed_attributes JOIN seed ON seed.id = seed_attributes.seedId')
        rawList = self.engine.execute(query).fetchall()
        return rawList, columnsNames

    def InsertDefaultListByRawSql(self, seedIdList):
        self.engine.execute(
            Seed.__table__.insert(),
            [{'seedId': seedId} for seedId in seedIdList])

    def Hello(self):
        print ('Hello, I\'m a repository')

    _seedRepository = SeedRepository()

    def __init__(self):
        super().__init__()
