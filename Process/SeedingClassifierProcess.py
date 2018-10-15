from Process import _BaseProcess as BaseProcess
from Repository.Classifier import _SeedingDataFrameRepository as SeedingDataFrameRepository
from Repository.Classifier import _ClassifierMetaRepository as ClassifierMetaRepository
from Repository.Classifier import _ResultsExportRepository as ResultsExportRepository
from Entity.Classifier import _ClassifierMeta as ClassifierMeta
from Entity.Classifier import _ResultsExport as ResultsExport
from constant import SeedAttributesNames, Contexts, ClassifiersNickNames
import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.grid_search import GridSearchCV

class SeedingClassifierProcess(BaseProcess):

    #region [Train Classifier]
    def TrainSeedClassifier(self, classifierNickname):
        try:
            self.logger.info('Train Seed Classifier started')
            
            self.logger.info('getting seeding-data-frame')
            seedingDataFrame = self._trainingSeedingDataFrameRepository.Get()
            
            self.logger.info('setup classifier')
            classifierMeta = self.CreateClassifierMeta(
                classifierSetterMethod = SeedingClassifierProcess.SelectClassifierSetup(classifierNickname))
            classifierMeta = self._classifierMetaRepository.StoreAndGet(classifierMeta)

            self.logger.info('train classifier')
            classifierMeta = self.TrainClassifier(classifierMeta, seedingDataFrame)
            classifierMeta = self._classifierMetaRepository.StoreAndGet(classifierMeta)

        except Exception as exception:
            self.logger.exception('Train Seed Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Train Seed Classifier finished')
            return classifierMeta
    
    def CreateClassifierMeta(self, classifierSetterMethod):
        self.logger.info('classifier: ' + str(classifierSetterMethod.__name__))
        definitionDictionary, classifier = classifierSetterMethod()
        definitionDictionary['classifierSettingsSummary'] = str(classifier)
        classifierMeta = ClassifierMeta(
            classifier = classifier,
            definitionDictionary = definitionDictionary)
        return classifierMeta

    def SelectClassifierSetup(classifierNickname):
        if(classifierNickname == ClassifiersNickNames.DECISION_TREE):
            return SeedingClassifierProcess.SetupDecisionTreeClassifier
        if(classifierNickname == ClassifiersNickNames.RANDOM_FOREST):
            return SeedingClassifierProcess.SetupRandomForestClassifier
        if(classifierNickname == ClassifiersNickNames.ADABOOST_DECISION_TREE):
            return SeedingClassifierProcess.SetupAdaboostClassifier
        return None

    def SetupAdaboostClassifier():
        definitionDictionary = {
            'type': 'emsemble estimator',
            'name': 'AdaBoost',
            'details': '',
            'baseEstimator': 'Decision Tree Classifier',
            'baseEstimatorDefinition': {
                'splitter': 'random',
                'max_depth': 5,
                'min_samples_leaf': 50
            },
            'algorithm': 'SAMME',
            'numberEstimators': 20
        }
        adaBoostClassifier = AdaBoostClassifier(
            DecisionTreeClassifier(
                splitter = definitionDictionary['baseEstimatorDefinition']['splitter'], 
                max_depth = definitionDictionary['baseEstimatorDefinition']['max_depth'],
                min_samples_leaf = definitionDictionary['baseEstimatorDefinition']['min_samples_leaf']
            ),
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
            'numberEstimators': 10
        }
        randomForestClassifier = RandomForestClassifier(n_estimators = definitionDictionary['numberEstimators'])
        return (definitionDictionary, randomForestClassifier)

    def TrainClassifier(self, classifierMeta, seedingDataFrame):
        classifier = classifierMeta.classifier
        attributesDataFrame = seedingDataFrame.dataFrame[SeedAttributesNames.ATTRIBUTES]
        targetClass = seedingDataFrame.dataFrame[SeedAttributesNames.TARGET_CLASS]
        classifier.fit(X = attributesDataFrame, y = targetClass)
        
        classifierMeta.attributesReport = SeedingClassifierProcess.GetAttributesReport(classifier)
        classifierMeta.graphviz = SeedingClassifierProcess.GetGraphviz(classifier)
        classifierMeta.summaryTrainData = seedingDataFrame.descriptionDictionary
        classifierMeta = self.UpdateDescriptionAndClassifier(classifierMeta, classifier)
        return classifierMeta

    def GetAttributesReport(classifier):
        if(isinstance(classifier, DecisionTreeClassifier)):
            return SeedingClassifierProcess.GetAttributesFromDecisionTree(classifier)
        if(isinstance(classifier, RandomForestClassifier)):
            return SeedingClassifierProcess.GetAttributesFromRandomForest(classifier)
        if(isinstance(classifier, AdaBoostClassifier)):
            return SeedingClassifierProcess.GetAttributesFromAdaBoost(classifier)
        return None
    
    def GetAttributesFromDecisionTree(decisionTreeClassifier):
        return {
            'feature_importances_': str(decisionTreeClassifier.feature_importances_),
            'max_features_': str(decisionTreeClassifier.max_features_),
            'classes_': str(decisionTreeClassifier.classes_),
            'n_classes_': str(decisionTreeClassifier.n_classes_),
            'n_features_': str(decisionTreeClassifier.n_features_),
            'n_outputs_': str(decisionTreeClassifier.n_outputs_)
        }
    
    def GetAttributesFromRandomForest(randomForestClassifier):
        return {
            'estimators_': [ 
                SeedingClassifierProcess.GetAttributesFromDecisionTree(decisionTreeClassifier)
                for decisionTreeClassifier in randomForestClassifier.estimators_],
            'classes_': str(randomForestClassifier.classes_),
            'n_classes_': str(randomForestClassifier.n_classes_),
            'n_features_': str(randomForestClassifier.n_features_),
            'n_outputs_': str(randomForestClassifier.n_outputs_),
            'feature_importances_': str(randomForestClassifier.feature_importances_)
        }

    def GetAttributesFromAdaBoost(adaBoostClassifier):
        return {
            'estimators_': [ 
                SeedingClassifierProcess.GetAttributesReport(estimator)
                for estimator in adaBoostClassifier.estimators_],
            'classes_': str(adaBoostClassifier.classes_),
            'n_classes_': str(adaBoostClassifier.n_classes_),
            'estimator_weights_': str(adaBoostClassifier.estimator_weights_),
            'estimator_errors_': str(adaBoostClassifier.estimator_errors_),
            'feature_importances_': str(adaBoostClassifier.feature_importances_)
        }        
    
    def GetGraphviz(classifier):
        if(isinstance(classifier, DecisionTreeClassifier)):
            return SeedingClassifierProcess.GetGraphvizFromDecisionTree(classifier)
        if(isinstance(classifier, RandomForestClassifier)):
            return SeedingClassifierProcess.GetGraphvizListFromRandomForest(classifier)
        if(isinstance(classifier, AdaBoostClassifier)):
            return SeedingClassifierProcess.GetGraphvizListFromAdaBoost(classifier)
        return None

    def GetGraphvizFromDecisionTree(decisionTreeClassifier):
        return tree.export_graphviz(decisionTreeClassifier, out_file=None, filled=True, rounded=True,
            special_characters=True, 
            class_names = list(map(lambda _class: str(_class),decisionTreeClassifier.classes_)), 
            feature_names = SeedAttributesNames.ATTRIBUTES, leaves_parallel = True)
        
    def GetGraphvizListFromRandomForest(randomForestClassifier):
        graphviz = []
        for decisionTree in randomForestClassifier.estimators_:
            graphviz.append(
                SeedingClassifierProcess.GetGraphvizFromDecisionTree(decisionTree))
        return graphviz

    def GetGraphvizListFromAdaBoost(adaBoostClassifier):
        graphviz = []
        for estimator in adaBoostClassifier.estimators_:
            graphviz.append(
                SeedingClassifierProcess.GetGraphviz(estimator))
        return graphviz
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
            seedingDataFrame = self._testingSeedingDataFrameRepository.Get()
            
            self.logger.info('getting classifier')
            classifierMeta = self._classifierMetaRepository.Get()
            
            self.logger.info('test classifier')
            classifierMeta, reportList = self.TestClassifier(classifierMeta, seedingDataFrame)
            classifierMeta = self._classifierMetaRepository.StoreAndGet(classifierMeta)

        except Exception as exception:
            self.logger.exception('Test Classifier failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Test Classifier finished')
            return reportList

    def TestClassifier(self, classifierMeta, seedingDataFrame):
        classifier = classifierMeta.classifier
        attributesDataFrame = seedingDataFrame.dataFrame[SeedAttributesNames.ATTRIBUTES]
        classifierPrediction = pandas.DataFrame(data = classifier.predict(X = attributesDataFrame),
            columns = ['classifierPrediction'], index = seedingDataFrame.dataFrame.index)
        
        expectedTargetClass = seedingDataFrame.dataFrame[SeedAttributesNames.TARGET_CLASS]
        report = classification_report(
            y_true = expectedTargetClass,
            y_pred = classifierPrediction)
        reportList = self.ConvertClassificationReportToList(report)
        classifierMeta.report = report
        classifierMeta.metaDataFrame = SeedingClassifierProcess.GetMetaDataFrame(
            expectedTargetClass, classifierPrediction, seedingDataFrame.dataFrame)
        classifierMeta.summaryTestData = seedingDataFrame.descriptionDictionary
        classifierMeta = self.UpdateDescriptionAndClassifier(classifierMeta, classifier)
        folderPath = self.ExportExperimentResults(classifierMeta)
        return classifierMeta, reportList

    def ConvertClassificationReportToList(self, report):
        reportData = []
        lines = report.split('\n')
        for line in lines[2:-3]:
            row = {}
            rowData = line.split()
            row['class'] = rowData[0]
            row['precision'] = float(rowData[1])
            row['recall'] = float(rowData[2])
            row['f1Score'] = float(rowData[3])
            row['support'] = float(rowData[4])
            reportData.append(row)
        return reportData

    def GetMetaDataFrame(expectedTargetClass, classifierPrediction, dataFrame):
        metaColumns = [
            columnName 
            for columnName in SeedAttributesNames.META 
            if(columnName in dataFrame.columns)]
        metaDataFrame = pandas.concat(
            [expectedTargetClass, classifierPrediction, dataFrame[metaColumns]],
            axis = 'columns')
        return metaDataFrame
    
    def ExportExperimentResults(self, classifierMeta = None):
        if classifierMeta is None:
            classifierMeta = self._classifierMetaRepository.Get()            
        resultsExport = ResultsExport(classifierMeta = classifierMeta)
        folderPath = self._resultsExportRepository.StoreReport(resultsExport = resultsExport)
        return folderPath
    #end_region [Test Classifier]

    def ExportClassifierGraphviz(self):
        classifierMeta = self._classifierMetaRepository.Get()
        classifierMeta.graphviz = SeedingClassifierProcess.GetGraphviz(classifierMeta.classifier)
        self.ExportExperimentResults(classifierMeta)

    def GridSearchAdaBoostDecisionTree(self):
        parameterGrid = {
            "base_estimator__criterion" : ["gini", "entropy"],
            "base_estimator__splitter" :   ["best", "random"],
            "base_estimator__max_depth" :   list(range(0, 16, 1))[1:],
            "n_estimators": list(range(0, 101, 10))[1:]}


        DTC = DecisionTreeClassifier(random_state = 11, max_features = "auto", class_weight = "auto",max_depth = None)

        ABC = AdaBoostClassifier(base_estimator = DTC)

        # run grid search
        grid_search_ABC = GridSearchCV(ABC, parameterGrid=parameterGrid, scoring = 'roc_auc')

    def __init__(self):
        self._trainingSeedingDataFrameRepository = SeedingDataFrameRepository(context = Contexts.TRAIN)
        self._testingSeedingDataFrameRepository = SeedingDataFrameRepository(context = Contexts.TEST)
        self._classifierMetaRepository = ClassifierMetaRepository()
        self._resultsExportRepository = ResultsExportRepository()
        super().__init__()
