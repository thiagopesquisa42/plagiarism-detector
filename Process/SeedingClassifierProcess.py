from Process import _BaseProcess as BaseProcess
from Process.Commom import _TextCollectionMetaCommom as TextCollectionMetaCommom
from Repository import _BaseRepository as BaseRepository
from Repository.Seeding import _SeedingDataRepository as SeedingDataRepository
from Repository.Seeding import _SeedAttributesRepository as SeedAttributesRepository
from Repository.Classifier import _SeedingDataFrameRepository as SeedingDataFrameRepository
from Repository.Classifier import _ClassifierMetaRepository as ClassifierMetaRepository
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Entity.Classifier import _SeedingDataFrame as SeedingDataFrame
from Entity.Classifier import _ClassifierMeta as ClassifierMeta
from constant import SeedAttributesNames
import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

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

            # [7] salvar dataframe de treino and
            # # [2] transform in dataFrame
            # self.logger.info('get seeds attributes')
            # seedingDataFrame = self.TransformInSeedingDataFrame(seedAttributesList, seedingData)
            # dataFrame = seedingDataFrame.getDataFrame()
 
            # [3] attributes selection
            # self.logger.info('attributes selection')
            # dataFrame = self.SelectColumnsInDataFrame(dataFrame)
            # self.UpdateSeedingDataFrame(seedingDataFrame, dataFrame)

            # [4] dataframe cleaning

            seedingDataFrame = self._seedingDataFrameRepository.Get(id = 2)
            dataFrame = seedingDataFrame.getDataFrame()
            # [9] criar e salvar pickle do classificador treinado
            # [6] salvar informações do classificador AdaBoost
            # [5] setup AdaBoost classifier
            self.logger.info('setup AdaBoost classifier')
            classifierMeta = self.CreateClassifierMeta(
                classifierSetterMethod = SeedingClassifierProcess.SetupAdaboostClassifier)

            # [8] treinar classificador de sementes
            

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
    
    def CreateClassifierMeta(self, classifierSetterMethod):
        definitionDictionary, classifier = classifierSetterMethod()
        classifierMeta = ClassifierMeta(definitionDictionary = definitionDictionary)
        classifierMeta.setPickleClassifier(classifier)
        self._baseRepository.Insert(classifierMeta)
        return classifierMeta

    def SetupAdaboostClassifier():
        definitionDictionary = {
            'baseEstimator': 'Decision Tree Classifier',
            'baseEstimatorDefinition': {
                'splitter': 'random'
            },
            'algorithm': 'SAMME',
            'numberEstimators': 200
        }
        adaBoostClassifier = AdaBoostClassifier(
            DecisionTreeClassifier(
                splitter = definitionDictionary['baseEstimatorDefinition']['splitter']),
            algorithm = definitionDictionary['algorithm'],
            n_estimators = definitionDictionary['numberEstimators'])
        return (definitionDictionary, adaBoostClassifier)

    _baseRepository = BaseRepository()
    _seedingDataRepository = SeedingDataRepository()
    _seedAttributesRepository = SeedAttributesRepository()
    _seedingDataFrameRepository = SeedingDataFrameRepository()
    _classifierMetaRepository = ClassifierMetaRepository()

    def __init__(self):
        super().__init__()
