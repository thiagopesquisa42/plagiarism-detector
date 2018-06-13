from Process import _BaseProcess as BaseProcess
from Process import _SeedingClassifierProcess as SeedingClassifierProcess
from Repository.Seeding import _SeedingDataRepository as SeedingDataRepository
from Repository.Classifier import _SeedingDataFrameRepository as SeedingDataFrameRepository
from Repository.Classifier import _ClassifierMetaRepository as ClassifierMetaRepository
from Entity.Classifier import _SeedingDataFrame as SeedingDataFrame
from Entity.Classifier import _ClassifierMeta as ClassifierMeta
from Entity import _PlagiarismClass as PlagiarismClass
from constant import SeedAttributesNames, Contexts
import pandas
from imblearn.combine import SMOTEENN

class SeedingDataProcess(BaseProcess):

    #region [Create Seeding DataFrame from Seeding Data started]
    def CreateSeedingDataFrameFromSeedingData(self):
        try:
            self.logger.info('Create Seeding DataFrame from Seeding Data started')
            self.logger.info('getting seeding data')
            seedingData = self._seedingDataRepository.Get()

            self.logger.info('transform seeds attributes in DataFrame')
            seedingDataFrame = self.TransformSeedAttributesInSeedingDataFrame(seedingData)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

            # self.logger.info('binarize target classes')
            # seedingDataFrame = self.BinarizeTargetClass(seedingDataFrame, classFalse = PlagiarismClass.none)
            # seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)
 
            # self.logger.info('attributes selection')
            # seedingDataFrame = self.SelectColumnsInDataFrame(seedingDataFrame)
            # seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

            # self.logger.info('attributes remove none rows')
            # seedingDataFrame = self.RemoveNoneValues(seedingDataFrame)
            # seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

            # if(self._context == Contexts.TRAIN):
            #     self.logger.info('remove meta columns')
            #     seedingDataFrame = self.RemoveMetaColumnsInDataFrame(seedingDataFrame)
                
            #     self.logger.info('attributes resample classes, only at train')
            #     seedingDataFrame = self.BalanceByResample(seedingDataFrame)
            #     # seedingDataFrame = self.BalanceBySmoteEnn(seedingDataFrame)
            #     seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

        except Exception as exception:
            self.logger.exception('Create Seeding DataFrame from Seeding Data failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Create Seeding DataFrame from Seeding Data finished')
            return seedingDataFrame
    
    def TransformSeedAttributesInSeedingDataFrame(self, seedingData):
        seedAttributesList = []
        for seedListPerRawTextPair in seedingData.listOfSeedListPerRawTextPair:
            seedAttributesList.extend([[seed.attributes.__dict__, seed, seedListPerRawTextPair.rawTextPair] for seed in seedListPerRawTextPair.seedList])
        for seedAttributes, seed, rawTextPair in seedAttributesList:
            seedAttributes.update({   
                SeedAttributesNames.Names.metaSeed: seed,
                SeedAttributesNames.Names.metaRawTextPair: rawTextPair})
        seedAttributesList = [
            seedAttributes 
            for seedAttributes, seed, rawTextPair in seedAttributesList]
        dataFrame = pandas.DataFrame.from_records(data = seedAttributesList)
        seedingDataFrame = self.CreateSeedingDataFrame(dataFrame)
        return seedingDataFrame

    def CreateSeedingDataFrame(self, dataFrame):
        descriptionDictionary = self.CreateDataFrameDescription(dataFrame)
        seedingDataFrame = SeedingDataFrame(
            dataFrame = dataFrame,
            descriptionDictionary = descriptionDictionary)
        return seedingDataFrame
    
    def CreateDataFrameDescription(self, dataFrame, appendToDescription = None):
        descriptionDictionary = {
            'summary': str(dataFrame.describe(include = 'all')),
        }
        if(appendToDescription is not None):
            descriptionDictionary.update(appendToDescription)
        return descriptionDictionary
    
    def UpdateDescriptionAndDataFrame(self, seedingDataFrame, dataFrame, appendToDescription = None):
        seedingDataFrame.dataFrame = dataFrame
        seedingDataFrame.descriptionDictionary.update(self.CreateDataFrameDescription(seedingDataFrame.dataFrame, appendToDescription))
        return seedingDataFrame

    def SelectColumnsInDataFrame(self, seedingDataFrame):
        dataFrame = seedingDataFrame.dataFrame
        removeAttributeNameList = SeedAttributesNames.REMOVE_LIST
        for attributeName in removeAttributeNameList:
            if attributeName in dataFrame.columns:
                del dataFrame[attributeName]
        seedingDataFrame = self.UpdateDescriptionAndDataFrame(seedingDataFrame, dataFrame,
            appendToDescription = {'removeAttributeNameList': removeAttributeNameList})
        return seedingDataFrame
    
    def RemoveMetaColumnsInDataFrame(self, seedingDataFrame):
        dataFrame = seedingDataFrame.dataFrame
        removeAttributeNameList = SeedAttributesNames.META
        for attributeName in removeAttributeNameList:
            if attributeName in dataFrame.columns:
                del dataFrame[attributeName]
        seedingDataFrame = self.UpdateDescriptionAndDataFrame(seedingDataFrame, dataFrame,
            appendToDescription = {'removed meta columns': removeAttributeNameList})
        return seedingDataFrame

    def RemoveNoneValues(self, seedingDataFrame):
        dataFrame = seedingDataFrame.dataFrame
        columns = [
            column
            for column in dataFrame.columns
            if(not column in SeedAttributesNames.META)]
        dataFrame = dataFrame.dropna(axis='index', how='any', subset = columns)
        seedingDataFrame = self.UpdateDescriptionAndDataFrame(seedingDataFrame, dataFrame,
            appendToDescription = {'removeNoneRows': 'remove row with None value at these columns ' + str(columns)})
        return seedingDataFrame
    #end_region [Create Seeding DataFrame from Seeding Data started]
    
    #region [Imbalanced Learning Methods]
    def BalanceBySmoteEnn(self, seedingDataFrame):
        dataFrame = seedingDataFrame.dataFrame
        balancer = SMOTEENN()
        X_resampled, y_resampled = balancer.fit_sample(
            X = dataFrame[SeedAttributesNames.ATTRIBUTES], 
            y = dataFrame[SeedAttributesNames.TARGET_CLASS])
        balancedDataFrame = pandas.concat(
            objs = [
                pandas.DataFrame(data = X_resampled, columns = SeedAttributesNames.ATTRIBUTES), 
                pandas.DataFrame(data = y_resampled, columns=[SeedAttributesNames.TARGET_CLASS])], 
            axis='columns')
        seedingDataFrame = self.UpdateDescriptionAndDataFrame(seedingDataFrame, balancedDataFrame,
                appendToDescription = {'balancing': 'classes balanced by combination of SMOTE and ENN'})
        return seedingDataFrame

    def BalanceByResample(self, seedingDataFrame):
        dataFrame = seedingDataFrame.dataFrame
        classesLengths = dataFrame.plagiarismClass.value_counts()
        minLength = min(classesLengths)
        maxLength = max(classesLengths)

        if(minLength != maxLength):
            balancedDataFrame = pandas.DataFrame()
            classes = dataFrame.plagiarismClass.unique()
            for thisClass in classes:
                dataFrameThisClassOnly = dataFrame[(dataFrame.plagiarismClass == thisClass)]
                dataFrameThisClassOnlyResampled = dataFrameThisClassOnly.sample(
                    n = minLength, replace = False, random_state = 42)
                balancedDataFrame = pandas.concat([balancedDataFrame, dataFrameThisClassOnlyResampled])
            seedingDataFrame = self.UpdateDescriptionAndDataFrame(seedingDataFrame, balancedDataFrame,
                appendToDescription = {'balancing': 'classes balanced by sub-sampling of oversampled classes'})
        return seedingDataFrame

    def Resample(self, seedingDataFrame, classToResample, numberOfSamples):
        dataFrame = seedingDataFrame.dataFrame
        dataFrameNoneClassOnly = dataFrame[(dataFrame.plagiarismClass == classToResample)]
        dataFrameNoneClassOnlyResampled = dataFrameNoneClassOnly.sample(
            n = numberOfSamples, replace = False, random_state = 42)
        dataFrameWithoutNoneClass = dataFrame[(dataFrame.plagiarismClass != classToResample)]
        dataFrame = pandas.concat([dataFrameWithoutNoneClass, dataFrameNoneClassOnlyResampled])
        seedingDataFrame = self.UpdateDescriptionAndDataFrame(seedingDataFrame, dataFrame,
            appendToDescription = {
                'resampling': 'arbitrary resample of class ' + str(classToResample),
                'numberOfSamplesInResampling': numberOfSamples})
        return seedingDataFrame
    #end_region [Imbalanced Learning Methods]

    #region [Alter Seeding DataFrame and store in new register]
    def AlterSeedingData(self):
        try:
            self.logger.info('[Alter Seeding DataFrame and store in new register]')
            seedingDataFrame = self._seedingDataFrameRepository.Get()
            
            self.logger.info('binarize target classes')
            seedingDataFrame = self.BinarizeTargetClass(seedingDataFrame, classFalse = PlagiarismClass.none)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)            
            
        except Exception as exception:
            self.logger.exception('[Alter Seeding DataFrame and store in new register] failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('[Alter Seeding DataFrame and store in new register] finish')
            return seedingDataFrame
    
    def BinarizeTargetClass(self, seedingDataFrame, classTrue = None, classFalse = None):
        if((classTrue is not None) and (classFalse is not None)):
            raise Exception(r"\
                To binarize specify only one of the boolean values, \
                the class to be treated as classTrue or \
                the class to be treated as classFalse")
        dataFrame = seedingDataFrame.dataFrame
        dataFrameBinaryPlagiarismClass = (dataFrame.plagiarismClass == classTrue) if classTrue is not None else (dataFrame.plagiarismClass != classFalse)
        dataFrame['plagiarismClass'] = dataFrameBinaryPlagiarismClass
        chosenClass = classTrue or classFalse
        seedingDataFrame = self.UpdateDescriptionAndDataFrame(seedingDataFrame, dataFrame, 
            appendToDescription = {
                'binarizeTargetClass': str('class True' if classTrue else 'class False') + ': ' + str(chosenClass)})
        return seedingDataFrame
    #end_region [Alter Seeding DataFrame and store in new register]

    def CreateSeedingDataFrameFromSeedingDataSummaryDriven(self):
        try:
            self.logger.info('Create Seeding DataFrame from Seeding Data [Summary-Driven] started')
            self.logger.info('getting seeding data')
            seedingData = self._seedingDataRepository.Get()

            self.logger.info('transform seeds attributes in DataFrame')
            seedingDataFrame = self.TransformSeedAttributesInSeedingDataFrame(seedingData)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

            self.logger.info('binarize target classes')
            seedingDataFrame = self.BinarizeTargetClass(seedingDataFrame, classTrue = PlagiarismClass.obfuscatedSummary)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

            self.logger.info('attributes resample class none')
            seedingDataFrame = self.BalanceByResample(seedingDataFrame)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)
 
            self.logger.info('attributes selection')
            seedingDataFrame = self.SelectColumnsInDataFrame(seedingDataFrame)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

            self.logger.info('attributes remove none rows')
            seedingDataFrame = self.RemoveNoneValues(seedingDataFrame)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

        except Exception as exception:
            self.logger.exception('Create Seeding DataFrame from Seeding Data [Summary-Driven] failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Create Seeding DataFrame from Seeding Data [Summary-Driven] finished')
            return seedingDataFrame

    def ExportIdealClassifier(self):
        try:
            self.logger.info('[Export ideal classifier] started')          
            seedingDataFrame = self._seedingDataFrameRepository.Get()
            classifierMeta = ClassifierMeta(None, {})
            classifierPrediction = pandas.DataFrame(
                data = seedingDataFrame.dataFrame[SeedAttributesNames.TARGET_CLASS].values,
                columns = ['classifierPrediction'], 
                index = seedingDataFrame.dataFrame.index)
            classifierMeta.metaDataFrame = SeedingClassifierProcess.GetMetaDataFrame(
                expectedTargetClass = seedingDataFrame.dataFrame[SeedAttributesNames.TARGET_CLASS], 
                classifierPrediction = classifierPrediction, 
                dataFrame = seedingDataFrame.dataFrame)
            classifierMeta = self._classifierMetaRepository.StoreAndGet(classifierMeta)
        except Exception as exception:
            self.logger.info('[Export ideal classifier] failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('[Export ideal classifier] finished')
            return classifierMeta

    def __init__(self, context):
        self._context = context
        self._seedingDataRepository = SeedingDataRepository(context)
        self._seedingDataFrameRepository = SeedingDataFrameRepository(context)
        self._classifierMetaRepository = ClassifierMetaRepository()
        self._seedingClassifierProcess = SeedingClassifierProcess()
        super().__init__()
