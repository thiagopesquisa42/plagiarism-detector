from Repository import _BaseRepository as BaseRepository
import os

class SeedingDataRepository(BaseRepository):
    name = 'SeedingDataRepository'

    def __init__(self):
        super().__init__()
        rootLocation = os.path.join(self.rootLocation, self.name)
