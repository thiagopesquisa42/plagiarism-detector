from Repository import _BaseRepository as BaseRepository
import os

class PreProcessedDataRepository(BaseRepository):
    name = 'PreProcessedDataRepository'

    def __init__(self):
        super().__init__()
        rootLocation = os.path.join(self.rootLocation, self.name)
