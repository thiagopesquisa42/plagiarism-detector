from Process import _BaseProcess as BaseProcess
from Process.Commom import _TextCollectionMetaCommom as TextCollectionMetaCommom
from Repository import _BaseRepository as BaseRepository
from Repository.Seeding import _SeedingDataRepository as SeedingDataRepository
from Repository.Seeding import _SeedAttributesRepository as SeedAttributesRepository
from Repository.Classifier import _SeedingDataFrameRepository as SeedingDataFrameRepository
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Entity.Classifier import _SeedingDataFrame as SeedingDataFrame
from constant import SeedAttributesNames
import pandas

class SeedingClassifierProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from SeedingClassifierProcess')
        print ('Hello, I\'m the SeedingClassifierProcess')

    def TrainSeedClassifier(self, seedingDataId):
        try:
            self.logger.info('Train Seed Classifier started')
            # # [0] check data reference
            # self.logger.info('check data set reference')
            # seedingData = self._seedingDataRepository.Get(id = seedingDataId)
            # TextCollectionMetaCommom.CheckPurpose(
            #     textCollectionMeta = seedingData.preProcessedData.textCollectionMeta,
            #     purpose = TextCollectionMetaPurpose.train
            # )

            # # [1] get data
            # self.logger.info('get seeds attributes')
            # seedAttributesList = self._seedAttributesRepository.GetListBySeedingData(seedingData)

            # # [2] transform in dataFrame
            # self.logger.info('get seeds attributes')
            # seedingDataFrame = self.TransformInSeedingDataFrame(seedAttributesList, seedingData)
            # dataFrame = seedingDataFrame.getDataFrame()
 
            seedingDataFrame = self._seedingDataFrameRepository.Get(id = 2)
            dataFrame = seedingDataFrame.getDataFrame()
            # [3] attributes selection
            self.logger.info('attributes selection')
            dataFrame = self.SelectColumnsInDataFrame(dataFrame)
            self.UpdateSeedingDataFrame(seedingDataFrame, dataFrame)

            # [4] limpeza do dataframe
            # [5] configurar classificador AdaBoost
            # [6] salvar informações do classificador AdaBoost
            # [7] salvar dataframe de treino
            # [8] treinar classificador de sementes
            # [9] criar e salvar pickle do classificador treinado

            print('')
        except Exception as exception:
            self.logger.error('Train Seed Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Train Seed Classifier finished')
    
    def TransformInSeedingDataFrame(self, seedAttributesList, seedingData):
        seedAttributesDictionaryList = [
            seedAttributes.ToDictionary()
            for seedAttributes in seedAttributesList]
        dataFrame = pandas.DataFrame.from_records(seedAttributesDictionaryList)
        seedingDataFrame = self.CreateSeedingDataFrame(dataFrame, seedingData)
        return seedingDataFrame

    def CreateSeedingDataFrame(self, dataFrame, seedingData):
        seedingDataFrame = SeedingDataFrame(seedingData = seedingData)
        seedingDataFrame.setPickleDataFrame(dataFrame)
        self._baseRepository.Insert(seedingDataFrame)
        return seedingDataFrame
    
    def UpdateSeedingDataFrame(self, seedingDataFrame, dataFrame):
        seedingDataFrame.setPickleDataFrame(dataFrame)
        self._baseRepository.Insert(seedingDataFrame)

    def SelectColumnsInDataFrame(self, dataFrame):
        for attributeName in SeedAttributesNames.REMOVE_LIST:
            del dataFrame[attributeName]
        return dataFrame
    
    _baseRepository = BaseRepository()
    _seedingDataRepository = SeedingDataRepository()
    _seedAttributesRepository = SeedAttributesRepository()
    _seedingDataFrameRepository = SeedingDataFrameRepository()

    def __init__(self):
        super().__init__()
