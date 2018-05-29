from Repository import _BaseRepository as BaseRepository
import settings
import os

class SeedingDataRepository(BaseRepository):
    name = 'SeedingData'

    def __init__(self):
        self.subFolder = settings.currentSubFolder
        super().__init__()
