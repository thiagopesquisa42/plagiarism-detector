from Process import _BaseProcess as BaseProcess
from Process.Commom import _TextCollectionMetaCommom as TextCollectionMetaCommom
from Repository import _BaseRepository as BaseRepository
from Repository.Seeding import _SeedingDataRepository as SeedingDataRepository
from Repository.Classifier import _SeedingDataFrameRepository as SeedingDataFrameRepository
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose
from Entity.Classifier import _SeedingDataFrame as SeedingDataFrame
from Entity.Classifier import _ClassifierMeta as ClassifierMeta
from Entity import _PlagiarismClass as PlagiarismClass
from constant import SeedAttributesNames
import pandas

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

            self.logger.info('binarize target classes')
            seedingDataFrame = self.BinarizeTargetClass(seedingDataFrame, classFalse = PlagiarismClass.none)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

            self.logger.info('attributes resample class none')
            # seedingDataFrame = self.Resample(seedingDataFrame, classToResample = 'none', numberOfSamples = 1000)
            seedingDataFrame = self.BalanceByResample(seedingDataFrame)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)
 
            self.logger.info('attributes selection')
            seedingDataFrame = self.SelectColumnsInDataFrame(seedingDataFrame)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

            self.logger.info('attributes remove none rows')
            seedingDataFrame = self.RemoveNoneValues(seedingDataFrame)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)

        except Exception as exception:
            self.logger.error('Create Seeding DataFrame from Seeding Data failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Create Seeding DataFrame from Seeding Data finished')
            return seedingDataFrame
    
    def TransformSeedAttributesInSeedingDataFrame(self, seedingData):
        seedAttributesList = []
        for seedListPerRawTextPair in seedingData.listOfSeedListPerRawTextPair:
            seedAttributesList.extend([seed.attributes.__dict__ for seed in seedListPerRawTextPair.seedList])
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
    
    def RemoveNoneValues(self, seedingDataFrame):
        dataFrame = seedingDataFrame.dataFrame
        dataFrame = dataFrame.dropna(axis='index', how='any')
        seedingDataFrame = self.UpdateDescriptionAndDataFrame(seedingDataFrame, dataFrame,
            appendToDescription = {'removeNoneRows': 'remove row with any None value'})
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
    #end_region [Create Seeding DataFrame from Seeding Data started]

    #region [Alter Seeding DataFrame and store in new register]
    def AlterSeedingData(self):
        try:
            self.logger.info('[Alter Seeding DataFrame and store in new register]')
            seedingDataFrame = self._seedingDataFrameRepository.Get()
            
            self.logger.info('binarize target classes')
            seedingDataFrame = self.BinarizeTargetClass(seedingDataFrame, classFalse = PlagiarismClass.none)
            seedingDataFrame = self._seedingDataFrameRepository.StoreAndGet(seedingDataFrame)            
            
        except Exception as exception:
            self.logger.error('[Alter Seeding DataFrame and store in new register] failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('[Alter Seeding DataFrame and store in new register] finish')
            return seedingDataFrame

    # def CloneSeedingDataFrame(self, seedingDataFrame):
    #     previousDescription = seedingDataFrame.descriptionDictionary
    #     seedingDataFrameClone = self.CreateSeedingDataFrame(dataFrame = seedingDataFrame.dataFrame)
    #     previousDescription.update(seedingDataFrameClone.descriptionDictionary)
    #     seedingDataFrameClone.descriptionDictionary = previousDescription
    #     return seedingDataFrameClone

    def BinarizeTargetClass(self, seedingDataFrame, classTrue = None, classFalse = None):
        if((classTrue is not None) and (classFalse is not None)):
            raise Exception(r"\
                To binarize specify only one of the boolean values, \
                the class to be treated as classTrue or \
                the class to be treated as classFalse")
        dataFrame = seedingDataFrame.dataFrame
        dataFrameBinaryPlagiarismClass = (dataFrame.plagiarismClass == classTrue) if classTrue is not None else (dataFrame.plagiarismClass != classFalse)
        dataFrame['plagiarismClass'] = dataFrameBinaryPlagiarismClass
        seedingDataFrame = self.UpdateDescriptionAndDataFrame(seedingDataFrame, dataFrame, 
            appendToDescription = {'binarizeTargetClass': 'chose class True or class False'})
        return seedingDataFrame
    #end_region [Alter Seeding DataFrame and store in new register]

    _seedingDataRepository = SeedingDataRepository()
    _seedingDataFrameRepository = SeedingDataFrameRepository()

    def __init__(self):
        super().__init__()
