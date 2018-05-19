from Process import _BaseProcess as BaseProcess
from Repository import _BaseRepository as BaseRepository

class SeedingClassifierProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from SeedingClassifierProcess')
        print ('Hello, I\'m the SeedingClassifierProcess')

    def TrainSeedClassifier(self, seedingDataId):
        try:
            self.logger.info('Train Seed Classifier started')

        except Exception as exception:
            self.logger.info('Train Seed Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Train Seed Classifier finished')
    
    #region [Create seeding data]

    #end_region [Create seeding data]
    
    _baseRepository = BaseRepository()

    def __init__(self):
        super().__init__()
