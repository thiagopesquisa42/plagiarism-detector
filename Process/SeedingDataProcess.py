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

            self.logger.info('attributes resample class none')
            seedingDataFrame = self.Resample(seedingDataFrame, classToResample = 'none', numberOfSamples = 1000)
 
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
    
    def UpdateStoreSeedingDataFrame(self, seedingDataFrame, dataFrame, removedAttributeNameList = []):
        seedingDataFrame.descriptionDictionary = self.CreateDataFrameDescription(dataFrame, removedAttributeNameList)
        seedingDataFrame = self.UpdateSeedingPickleDataFrame(seedingDataFrame, dataFrame)
        # self._baseRepository.Insert(seedingDataFrame)
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
    
    def Resample(self, seedingDataFrame, classToResample, numberOfSamples):
        dataFrame = seedingDataFrame.GetDataFrame()
        
        dataFrameNoneClassOnly = dataFrame[(dataFrame.plagiarismClass == classToResample)]
        dataFrameNoneClassOnlyResampled = dataFrameNoneClassOnly.sample(
            n = numberOfSamples, replace = False, random_state = 42)
        dataFrameWithoutNoneClass = dataFrame[(dataFrame.plagiarismClass != classToResample)]
        dataFrame = pandas.concat([dataFrameWithoutNoneClass, dataFrameNoneClassOnlyResampled])
        
        seedingDataFrame = self.UpdateStoreSeedingDataFrame(seedingDataFrame, dataFrame)
        return seedingDataFrame
    #end_region [Create Seeding DataFrame from Seeding Data started]

    _baseRepository = BaseRepository()
    _seedingDataRepository = SeedingDataRepository()
    _seedAttributesRepository = SeedAttributesRepository()
    _seedingDataFrameRepository = SeedingDataFrameRepository()
    _classifierMetaRepository = ClassifierMetaRepository()

    def __init__(self):
        super().__init__()
