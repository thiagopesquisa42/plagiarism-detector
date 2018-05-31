from Repository import _BaseRepository as BaseRepository

class SeedingDataFrameRepository(BaseRepository):
    def __init__(self, context):
        super().__init__(context, name = 'SeedingDataFrame')
