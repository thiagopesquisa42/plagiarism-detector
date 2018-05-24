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
from Entity import _PlagiarismClass as PlagiarismClass
from constant import SeedAttributesNames
import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

class SeedingDataProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from SeedingDataProcess')
        print ('Hello, I\'m the SeedingDataProcess')

    #region [Create Seeding DataFrame from Seeding Data started]
    def CreateSeedingDataFrameFromSeedingData(self, seedingDataId, textCollectionMetaPurpose):
        try:
            self.logger.info('Create Seeding DataFrame from Seeding Data started')
            self.logger.info('check data set reference')
            seedingData = self._seedingDataRepository.Get(id = seedingDataId)
            TextCollectionMetaCommom.CheckPurpose(
                textCollectionMeta = seedingData.preProcessedData.textCollectionMeta,
                purpose = textCollectionMetaPurpose
            )

            self.logger.info('transform seeds attributes in DataFrame')
            seedingDataFrame = self.TransformSeedAttributesInSeedingDataFrame(seedingData)

            self.logger.info('binarize target classes')
            seedingDataFrame = self.BinarizeTargetClass(seedingDataFrame, classFalse = PlagiarismClass.none.name)

            self.logger.info('attributes resample class none')
            # seedingDataFrame = self.Resample(seedingDataFrame, classToResample = 'none', numberOfSamples = 1000)
            seedingDataFrame = self.BalanceByResample(seedingDataFrame)
 
            self.logger.info('attributes selection')
            seedingDataFrame = self.SelectColumnsInDataFrame(seedingDataFrame)

            self.logger.info('attributes remove none rows')
            seedingDataFrame = self.RemoveNoneValues(seedingDataFrame)
            self._baseRepository.Insert(seedingDataFrame)

        except Exception as exception:
            self.logger.error('Create Seeding DataFrame from Seeding Data failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('Create Seeding DataFrame from Seeding Data finished')
            return seedingDataFrame
    
    def TransformSeedAttributesInSeedingDataFrame(self, seedingData):
        seedAttributesList, columnsNames = self._seedAttributesRepository.GetRawListAllFieldsBySeedingData(seedingData)
        dataFrame = pandas.DataFrame.from_records(columns = columnsNames, data = seedAttributesList)
        seedingDataFrame = self.CreateSeedingDataFrame(dataFrame, seedingData)
        return seedingDataFrame

    def CreateSeedingDataFrame(self, dataFrame, seedingData):
        descriptionDictionary = self.CreateDataFrameDescription(dataFrame)
        seedingDataFrame = SeedingDataFrame(
            seedingData = seedingData,
            descriptionDictionary = descriptionDictionary)
        seedingDataFrame = self.UpdateSeedingPickleDataFrame(seedingDataFrame, dataFrame)
        # self._baseRepository.Insert(seedingDataFrame)
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
    
    def UpdateDescriptionAndPickleSeedingDataFrame(self, seedingDataFrame, dataFrame, removedAttributeNameList = []):
        seedingDataFrame.descriptionDictionary = self.CreateDataFrameDescription(dataFrame, removedAttributeNameList)
        seedingDataFrame = self.UpdateSeedingPickleDataFrame(seedingDataFrame, dataFrame)
        return seedingDataFrame

    def SelectColumnsInDataFrame(self, seedingDataFrame):
        dataFrame = seedingDataFrame.GetDataFrame()
        removeAttributeNameList = SeedAttributesNames.REMOVE_LIST
        for attributeName in removeAttributeNameList:
            del dataFrame[attributeName]
        seedingDataFrame = self.UpdateDescriptionAndPickleSeedingDataFrame(seedingDataFrame, dataFrame, 
            removedAttributeNameList = removeAttributeNameList)
        return seedingDataFrame
    
    def RemoveNoneValues(self, seedingDataFrame):
        dataFrame = seedingDataFrame.GetDataFrame()
        dataFrame = dataFrame.dropna(axis='index', how='any')
        seedingDataFrame = self.UpdateDescriptionAndPickleSeedingDataFrame(seedingDataFrame, dataFrame)
        return seedingDataFrame
    
    def BalanceByResample(self, seedingDataFrame):
        dataFrame = seedingDataFrame.GetDataFrame()
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
            seedingDataFrame = self.UpdateDescriptionAndPickleSeedingDataFrame(seedingDataFrame, balancedDataFrame)
        return seedingDataFrame

    def Resample(self, seedingDataFrame, classToResample, numberOfSamples):
        dataFrame = seedingDataFrame.GetDataFrame()
        dataFrameNoneClassOnly = dataFrame[(dataFrame.plagiarismClass == classToResample)]
        dataFrameNoneClassOnlyResampled = dataFrameNoneClassOnly.sample(
            n = numberOfSamples, replace = False, random_state = 42)
        dataFrameWithoutNoneClass = dataFrame[(dataFrame.plagiarismClass != classToResample)]
        dataFrame = pandas.concat([dataFrameWithoutNoneClass, dataFrameNoneClassOnlyResampled])
        seedingDataFrame = self.UpdateDescriptionAndPickleSeedingDataFrame(seedingDataFrame, dataFrame)
        return seedingDataFrame
    #end_region [Create Seeding DataFrame from Seeding Data started]

    #region [Alter Seeding DataFrame and store in new register]
    def AlterSeedingData(self, seedingDataFrame):
        try:
            self.logger.info('[Alter Seeding DataFrame and store in new register]')
            
            self.logger.info('clone DataFrame')
            seedingDataFrame = self.CloneSeedingDataFrame(seedingDataFrame)
            
            self.logger.info('binarize target classes')
            seedingDataFrame = self.BinarizeTargetClass(seedingDataFrame, classFalse = PlagiarismClass.none.name)
            
            self._baseRepository.Insert(seedingDataFrame)
        except Exception as exception:
            self.logger.error('[Alter Seeding DataFrame and store in new register] failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('[Alter Seeding DataFrame and store in new register] finish')
            return seedingDataFrame

    def CloneSeedingDataFrame(self, seedingDataFrame):
        seedingDataFrameClone = SeedingDataFrame(
            seedingData = seedingDataFrame.seedingData)
        dataFrame = seedingDataFrame.GetDataFrame()
        seedingDataFrameClone = self.UpdateDescriptionAndPickleSeedingDataFrame(
            seedingDataFrameClone, dataFrame)
        return seedingDataFrameClone

    def BinarizeTargetClass(self, seedingDataFrame, classTrue = None, classFalse = None):
        if((classTrue is not None) and (classFalse is not None)):
            raise Exception(r"\
                To binarize specify only one of the boolean values, \
                the class to be treated as classTrue or \
                the class to be treated as classFalse")
        dataFrame = seedingDataFrame.GetDataFrame()
        dataFrameBinaryPlagiarismClass = (dataFrame.plagiarismClass == classTrue) if classTrue is not None else (dataFrame.plagiarismClass != classFalse)
        dataFrame['plagiarismClass'] = dataFrameBinaryPlagiarismClass
        seedingDataFrame = self.UpdateDescriptionAndPickleSeedingDataFrame(seedingDataFrame, dataFrame)
        return seedingDataFrame

    #end_region [Alter Seeding DataFrame and store in new register]

    _baseRepository = BaseRepository()
    _seedingDataRepository = SeedingDataRepository()
    _seedAttributesRepository = SeedAttributesRepository()
    _seedingDataFrameRepository = SeedingDataFrameRepository()
    _classifierMetaRepository = ClassifierMetaRepository()

    def __init__(self):
        super().__init__()
