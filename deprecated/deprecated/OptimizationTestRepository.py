import Repository.DataBaseConfiguration as DataBaseConfiguration
from Repository import _BaseRepository as BaseRepository
from Entity.Seeding import _Seed as Seed
from sqlalchemy import create_engine

class OptimizationTestRepository():

    def GetOptimizedSeedList(self):
        r = self.engine.execute(
            Seed.__table__.select(whereclause = "id = 1")
        )
        print(r)
        s = Seed()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        self.engine = create_engine(DataBaseConfiguration.CONSTANTS_CONFIGURATIONS.
            SQLALCHEMY_CONNECTION_STRING_DATA_BASE, echo=False)
