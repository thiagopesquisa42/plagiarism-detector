from Repository import _BaseRepository as BaseRepository
from Entity.Classifier import _SeedingDataFrame as SeedingDataFrame

class SeedingDataFrameRepository(BaseRepository):
    def Get(self, id):
        return self.session.query(SeedingDataFrame).filter(SeedingDataFrame.id == id).first()

    def GetByRawSql(self, id):
        seedingDataFrameRaw = self.engine.execute(
            SeedingDataFrame.__table__.select(whereclause = "id = " + str(id))
        ).fetchone()
        seedingDataFrame = SeedingDataFrame(
            id = seedingDataFrameRaw[SeedingDataFrame.id.name],
            seedingDataId = seedingDataFrameRaw[SeedingDataFrame.seedingDataId.name],
            pickleDataFrame = seedingDataFrameRaw[SeedingDataFrame.pickleDataFrame.name])
        return seedingDataFrame

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
