from Process import _BaseProcess as BaseProcess
from Process.Commom import _TextCollectionMetaCommom as TextCollectionMetaCommom
from Repository import _BaseRepository as BaseRepository
from Repository.Seeding import _SeedingDataRepository as SeedingDataRepository
from Repository.Seeding import _SeedAttributesRepository as SeedAttributesRepository
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose

class SeedingClassifierProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from SeedingClassifierProcess')
        print ('Hello, I\'m the SeedingClassifierProcess')

    def TrainSeedClassifier(self, seedingDataId):
        try:
            self.logger.info('Train Seed Classifier started')
            # [0] validar referencia aos dados
            self.logger.info('check data set reference')
            seedingData = self._seedingDataRepository.Get(id = seedingDataId)
            TextCollectionMetaCommom.CheckPurpose(
                textCollectionMeta = seedingData.preProcessedData.textCollectionMeta,
                purpose = TextCollectionMetaPurpose.train
            )
            
            # [1] obter dados
            self.logger.info('get seeds attributes')
            seedAttributesList = self._seedAttributesRepository.GetListBySeedingData(seedingData)

            # [2] transformação
            # [3] seleção de atributos
            # [4] limpeza do dataframe
            # [5] configurar classificador AdaBoost
            # [6] salvar informações do classificador AdaBoost
            # [7] salvar dataframe de treino
            # [8] treinar classificador de sementes
            # [9] criar e salvar pickle do classificador treinado

            print('')
        except Exception as exception:
            self.logger.info('Train Seed Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Train Seed Classifier finished')
    
    #region [Create seeding data]

    #end_region [Create seeding data]
    
    _baseRepository = BaseRepository()
    _seedingDataRepository = SeedingDataRepository()
    _seedAttributesRepository = SeedAttributesRepository()

    def __init__(self):
        super().__init__()
