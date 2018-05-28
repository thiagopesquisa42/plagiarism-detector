import util
from Process import _SeedingClassifierProcess as SeedingClassifierProcess

_seedingClassifierProcess = SeedingClassifierProcess()
# classifierMetaTrained = _seedingClassifierProcess.TrainSeedClassifier()
classifierMetaTested = _seedingClassifierProcess.TestSeedClassifier()
print('finished')