from Repository import _BaseRepository as BaseRepository
import settings
import os

class SeedingDataFrameRepository(BaseRepository):
    name = 'SeedingDataFrame'

    def __init__(self):
        self.subFolder = settings.currentSubFolder
        super().__init__()