import util
from Process import _SeedingDataProcess as SeedingDataProcess

_seedingDataProcess = SeedingDataProcess()
dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingData()
print('finished')