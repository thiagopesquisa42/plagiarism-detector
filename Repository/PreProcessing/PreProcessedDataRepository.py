from Repository import _BaseRepository as BaseRepository

class PreProcessedDataRepository(BaseRepository):
    def __init__(self, context):
        super().__init__(context, name = 'PreProcessedData')
