from Process import _BaseProcess as BaseProcess
from Repository.Classifier import _SeedingDataFrameRepository as SeedingDataFrameRepository
from Repository.Classifier import _ClassifierMetaRepository as ClassifierMetaRepository
from Repository.Classifier import _ExperimentMetaRepository as ExperimentMetaRepository
from Entity.Classifier import _ClassifierMeta as ClassifierMeta
from Entity.Classifier import _ExperimentMeta as ExperimentMeta
from constant import SeedAttributesNames
import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import classification_report

class SeedingClassifierProcess(BaseProcess):

    #region [Train Classifier]
    def TrainSeedClassifier(self):
        try:
            self.logger.info('Train Seed Classifier started')
            
            self.logger.info('getting seeding-data-frame')
            seedingDataFrame = self._seedingDataFrameRepository.Get()
            
            self.logger.info('setup classifier')
            classifierMeta = self.CreateClassifierMeta(
                classifierSetterMethod = SeedingClassifierProcess.SetupRandomForestClassifier)
            classifierMeta = self._classifierMetaRepository.StoreAndGet(classifierMeta)

            self.logger.info('train classifier')
            classifierMeta = self.TrainClassifier(classifierMeta, seedingDataFrame)
            classifierMeta = self._classifierMetaRepository.StoreAndGet(classifierMeta)

        except Exception as exception:
            self.logger.error('Train Seed Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Train Seed Classifier finished')
            return classifierMeta
    
    def CreateClassifierMeta(self, classifierSetterMethod):
        self.logger.info('classifier: ' + str(classifierSetterMethod.__name__))
        definitionDictionary, classifier = classifierSetterMethod()
        classifierMeta = ClassifierMeta(
            classifier = classifier,
            definitionDictionary = definitionDictionary)
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
        classifier = classifierMeta.classifier
        dataFrame = seedingDataFrame.dataFrame
        targetClass = dataFrame[SeedAttributesNames.TARGET_CLASS]
        del dataFrame[SeedAttributesNames.TARGET_CLASS]
        trainAttributes = dataFrame
        classifier.fit(X = trainAttributes, y = targetClass)
        classifierMeta = self.UpdateDescriptionAndClassifier(classifierMeta, classifier, 
            appendToDefinition = {
                'train-seeding-data-frame-description': seedingDataFrame.descriptionDictionary})
        return classifierMeta
    #end_region [Train Classifier]

    def UpdateDescriptionAndClassifier(self, classifierMeta, classifier, appendToDefinition = None):
        classifierMeta.classifier = classifier
        if(appendToDefinition is not None):
            classifierMeta.definitionDictionary.update(appendToDefinition)
        return classifierMeta

    #region [Test Classifier]
    def TestSeedClassifier(self):
        try:
            self.logger.info('Test Classifier started')

            self.logger.info('getting seeding-data-frame')
            seedingDataFrame = self._seedingDataFrameRepository.Get()
            
            self.logger.info('getting classifier')
            classifierMeta = self._classifierMetaRepository.Get()
            
            self.logger.info('test classifier')
            classifierMeta = self.TestClassifier(classifierMeta, seedingDataFrame)
            classifierMeta = self._classifierMetaRepository.StoreAndGet(classifierMeta)

        except Exception as exception:
            self.logger.error('Test Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Test Classifier finished')
            return classifierMeta

    def TestClassifier(self, classifierMeta, seedingDataFrame):
        classifier = classifierMeta.classifier
        dataFrame = seedingDataFrame.dataFrame
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
        classifierMeta.report = report
        classifierMeta.expectedPredictedList = expectedPredictedDataFrame
        classifierMeta = self.UpdateDescriptionAndClassifier(classifierMeta, classifier, 
            appendToDefinition = {
                'test-seeding-data-frame-description': seedingDataFrame.descriptionDictionary})
        self.SaveExperimentResults(classifierMeta)
        return classifierMeta
    
    def SaveExperimentResults(self, classifierMeta):
        experimentMeta = ExperimentMeta(classifierMeta = classifierMeta)
        self._experimentMetaRepository.StoreReport(report = experimentMeta.report)
    #end_region [Test Classifier]


    def __init__(self):
        self._seedingDataFrameRepository = SeedingDataFrameRepository()
        self._classifierMetaRepository = ClassifierMetaRepository()
        self._experimentMetaRepository = ExperimentMetaRepository()
        super().__init__()
