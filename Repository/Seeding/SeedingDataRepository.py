from Repository import _BaseRepository as BaseRepository

class SeedingDataRepository(BaseRepository):
    def __init__(self, context):
        super().__init__(context, name = 'SeedingData')
