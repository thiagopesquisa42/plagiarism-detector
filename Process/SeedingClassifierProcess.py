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

            # # [2] transform in dataFrame
            # self.logger.info('get seeds attributes')
            # seedingDataFrame = self.TransformInSeedingDataFrame(seedAttributesList, seedingData)
 
            # # [3] attributes selection
            # self.logger.info('attributes selection')
            # seedingDataFrame = self.SelectColumnsInDataFrame(seedingDataFrame)

            seedingDataFrame = self._seedingDataFrameRepository.Get(id = 3)
            # # [4] dataframe cleaning
            seedingDataFrame = self.RemoveNoneValues(seedingDataFrame)

            # # [5] setup AdaBoost classifier
            # self.logger.info('setup AdaBoost classifier')
            # classifierMeta = self.CreateClassifierMeta(
            #     classifierSetterMethod = SeedingClassifierProcess.SetupAdaboostClassifier)

            classifierMeta = self._classifierMetaRepository.Get(id = 2)
            # [8] train classifier
            self.logger.info('train classifier')
            classifierMeta = self.TrainClassifier(classifierMeta, seedingDataFrame)

        except Exception as exception:
            self.logger.error('Train Seed Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Train Seed Classifier finished')
            print('')
    
    def TransformInSeedingDataFrame(self, seedAttributesList, seedingData):
        seedAttributesDictionaryList = [
            seedAttributes.ToDictionary()
            for seedAttributes in seedAttributesList]
        dataFrame = pandas.DataFrame.from_records(seedAttributesDictionaryList)
        seedingDataFrame = self.CreateSeedingDataFrame(dataFrame, seedingData)
        return seedingDataFrame

    def CreateSeedingDataFrame(self, dataFrame, seedingData):
        descriptionDictionary = self.CreateDataFrameDescription(dataFrame)
        seedingDataFrame = SeedingDataFrame(
            seedingData = seedingData,
            descriptionDictionary = descriptionDictionary)
        seedingDataFrame = self.UpdateSeedingPickleDataFrame(seedingDataFrame, dataFrame)
        self._baseRepository.Insert(seedingDataFrame)
        return seedingDataFrame
    
    def CreateDataFrameDescription(self, dataFrame, removedAttributeNameList = []):
        descriptionDictionary = {
            'summary': str(dataFrame.describe()),
            'removedAttributeNameList': removedAttributeNameList
        }
        return descriptionDictionary
    
    def UpdateSeedingPickleDataFrame(self, seedingDataFrame, dataFrame):
        seedingDataFrame.SetPickleDataFrame(dataFrame)
        return seedingDataFrame
    
    def UpdateStoreSeedingDataFrame(self, seedingDataFrame, dataFrame, removedAttributeNameList = []):
        seedingDataFrame.descriptionDictionary = self.CreateDataFrameDescription(dataFrame, removedAttributeNameList)
        seedingDataFrame = self.UpdateSeedingPickleDataFrame(seedingDataFrame, dataFrame)
        self._baseRepository.Insert(seedingDataFrame)
        return seedingDataFrame

    def SelectColumnsInDataFrame(self, seedingDataFrame):
        dataFrame = seedingDataFrame.GetDataFrame()
        removeAttributeNameList = SeedAttributesNames.REMOVE_LIST
        for attributeName in removeAttributeNameList:
            del dataFrame[attributeName]
        seedingDataFrame = self.UpdateStoreSeedingDataFrame(seedingDataFrame, dataFrame, 
            removedAttributeNameList = removeAttributeNameList)
        return seedingDataFrame
    
    def RemoveNoneValues(self, seedingDataFrame):
        dataFrame = seedingDataFrame.GetDataFrame()
        dataFrame = dataFrame.dropna(axis='index', how='any')
        seedingDataFrame = self.UpdateStoreSeedingDataFrame(seedingDataFrame, dataFrame)
        return seedingDataFrame
    
    def CreateClassifierMeta(self, classifierSetterMethod):
        definitionDictionary, classifier = classifierSetterMethod()
        classifierMeta = ClassifierMeta(definitionDictionary = definitionDictionary)
        classifierMeta.SetPickleClassifier(classifier)
        self._baseRepository.Insert(classifierMeta)
        return classifierMeta

    def SetupAdaboostClassifier():
        definitionDictionary = {
            'type': 'emsemble estimator',
            'name': 'AdaBoost',
            'details': '',
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

    def TrainClassifier(self, classifierMeta, seedingDataFrame):
        classifier = classifierMeta.GetClassifier()
        dataFrame = seedingDataFrame.GetDataFrame()
        targetClass = dataFrame[SeedAttributesNames.TARGET_CLASS]
        del dataFrame[SeedAttributesNames.TARGET_CLASS]
        trainAttributes = dataFrame
        classifier.fit(X = trainAttributes, y = targetClass)

        classifierMeta.SetPickleClassifier(classifier)
        classifierMeta.seedingDataFrame = seedingDataFrame
        self._baseRepository.Insert(classifierMeta)
        return classifierMeta

    _baseRepository = BaseRepository()
    _seedingDataRepository = SeedingDataRepository()
    _seedAttributesRepository = SeedAttributesRepository()
    _seedingDataFrameRepository = SeedingDataFrameRepository()
    _classifierMetaRepository = ClassifierMetaRepository()

    def __init__(self):
        super().__init__()
