from Repository import _BaseRepository as BaseRepository
import settings
import os

class PreProcessedDataRepository(BaseRepository):
    name = 'PreProcessedData'

    def __init__(self):
        self.subFolder = settings.currentSubFolder
        super().__init__()