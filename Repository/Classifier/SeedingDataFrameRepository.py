from Repository import _BaseRepository as BaseRepository
import os

class SeedingDataFrameRepository(BaseRepository):
    name = 'SeedingDataFrameRepository'

    def __init__(self):
        super().__init__()
        rootLocation = os.path.join(self.rootLocation, self.name)
