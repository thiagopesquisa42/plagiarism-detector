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
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import classification_report

class SeedingClassifierProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from SeedingClassifierProcess')
        print ('Hello, I\'m the SeedingClassifierProcess')

    #region [Train Classifier]
    def TrainSeedClassifier(self, seedingDataFrame):
        try:
            self.logger.info('Train Seed Classifier started')
            
            self.logger.info('check data set reference')
            #seedingDataFrame = self._seedingDataFrameRepository.GetByRawSql(id = seedingDataFrameId)
            seedingData = self._seedingDataRepository.Get(id = seedingDataFrame.seedingDataId)
            TextCollectionMetaCommom.CheckPurpose(
                textCollectionMeta = seedingData.preProcessedData.textCollectionMeta,
                purpose = TextCollectionMetaPurpose.train
            )

            self.logger.info('setup AdaBoost classifier')
            classifierMeta = self.CreateClassifierMeta(
                classifierSetterMethod = SeedingClassifierProcess.SetupAdaboostClassifier)

            self.logger.info('train classifier')
            classifierMeta = self.TrainClassifier(classifierMeta, seedingDataFrame)

        except Exception as exception:
            self.logger.error('Train Seed Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Train Seed Classifier finished')
            return classifierMeta
    
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
            'numberEstimators': 100
        }
        adaBoostClassifier = AdaBoostClassifier(
            DecisionTreeClassifier(
                splitter = definitionDictionary['baseEstimatorDefinition']['splitter']),
            algorithm = definitionDictionary['algorithm'],
            n_estimators = definitionDictionary['numberEstimators'])
        return (definitionDictionary, adaBoostClassifier)

    def SetupDecisionTreeClassifier():
        definitionDictionary = {
            'type': 'estimator',
            'name': 'Decision Tree',
            'details': 'default values of sktlearn library'
        }
        decisionTreeClassifier = DecisionTreeClassifier()
        return (definitionDictionary, decisionTreeClassifier)

    def SetupRandomForestClassifier():
        definitionDictionary = {
            'type': 'emsemble estimator',
            'name': 'Random Forest',
            'details': 'default settings',
            'baseEstimator': 'Decision Tree',
            'baseEstimatorDefinition': {
                'details': 'default values'
            },
            'numberEstimators': 100
        }
        randomForestClassifier = RandomForestClassifier(n_estimators = definitionDictionary['numberEstimators'])
        return (definitionDictionary, randomForestClassifier)

    def TrainClassifier(self, classifierMeta, seedingDataFrame):
        classifier = classifierMeta.GetClassifier()
        dataFrame = seedingDataFrame.GetDataFrame()
        targetClass = dataFrame[SeedAttributesNames.TARGET_CLASS]
        del dataFrame[SeedAttributesNames.TARGET_CLASS]
        trainAttributes = dataFrame
        classifier.fit(X = trainAttributes, y = targetClass)

        classifierMeta.SetPickleClassifier(classifier)
        classifierMeta.seedingDataFrameId = seedingDataFrame.id
        self._baseRepository.Insert(classifierMeta)
        # self._classifierMetaRepository.UpdateByRawSql(classifierMeta)
        return classifierMeta
    #end_region [Train Classifier]

    #region [Test Classifier]
    def TestSeedClassifier(self, seedingDataFrame, classifierMeta):
        try:
            self.logger.info('Test Classifier started')
            # [0] check data reference
            self.logger.info('check data set reference')
            #seedingDataFrame = self._seedingDataFrameRepository.GetByRawSql(id = seedingDataFrameId)
            seedingData = self._seedingDataRepository.Get(id = seedingDataFrame.seedingDataId)
            TextCollectionMetaCommom.CheckPurpose(
                textCollectionMeta = seedingData.preProcessedData.textCollectionMeta,
                purpose = TextCollectionMetaPurpose.test
            )

            # self.logger.info('get AdaBoost classifier')
            #classifierMeta = self._classifierMetaRepository.Get(id = classifierMetaId)

            self.logger.info('test classifier')
            classifierMeta = self.TestClassifier(classifierMeta, seedingDataFrame)

        except Exception as exception:
            self.logger.error('Test Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Test Classifier finished')
            return classifierMeta

    def TestClassifier(self, classifierMeta, seedingDataFrame):
        classifier = classifierMeta.GetClassifier()
        dataFrame = seedingDataFrame.GetDataFrame()
        expectedTargetClass = dataFrame[SeedAttributesNames.TARGET_CLASS]
        del dataFrame[SeedAttributesNames.TARGET_CLASS]
        testAttributes = dataFrame
        predictionList = classifier.predict(X = testAttributes)
        
        expectedPredictedDataFrame = pandas.DataFrame()
        expectedPredictedDataFrame['expected'] = expectedTargetClass
        expectedPredictedDataFrame['predicted'] = predictionList

        report = classification_report(
            y_true = expectedPredictedDataFrame['expected'],
            y_pred = expectedPredictedDataFrame['predicted'])
        print( report )
        classifierMeta.SetPickleExpectedPredictedList(expectedPredictedDataFrame)
        self._baseRepository.Insert(classifierMeta)
        # self._classifierMetaRepository.UpdateByRawSql(classifierMeta)
        return classifierMeta
    #end_region [Test Classifier]

    _baseRepository = BaseRepository()
    _seedingDataRepository = SeedingDataRepository()
    _seedAttributesRepository = SeedAttributesRepository()
    _seedingDataFrameRepository = SeedingDataFrameRepository()
    _classifierMetaRepository = ClassifierMetaRepository()

    def __init__(self):
        super().__init__()
