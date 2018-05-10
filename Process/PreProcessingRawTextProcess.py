from Process import _BaseProcess as BaseProcess
from Repository.PreProcessing import _PreProcessedDataRepository as PreProcessedDataRepository
from Entity.PreProcessing import _PreProcessedData as PreProcessedData

from constant import StopWord
import nltk
import re
from collections import Counter

class PreProcessingRawTextProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from PreProcessingRawTextProcess')
        print ('Hello, I\'m the PreProcessingRawTextProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')
        self._rawTextInternalProcess.Hello()

    def PreProcessing(self, textCollectionMetaId):
        try:
            self.logger.info('PreProcessing started')
            dataBase = self.CreatePreProcessedDataBaseIdentifier()
            print(dataBase.id)
            # [Z]
            # 1. create data base preprocessed id 
            # 2. create pp-step-chain node
            # 3. store pp-step configuration of the node
            # 4. store pp-step-chain node
            # 5. start tokenize in sentences step 
            # 6. for each raw text, create a sentence list

        except Exception as exception:
            self.logger.info('PreProcessing failure: ' + str(exception))
        else:
            self.logger.info('PreProcessing finished')

    def CreatePreProcessedDataBaseIdentifier(self):
        dataBase = PreProcessedData()
        self._preProcessedDataRepository.Insert(dataBase)
        return dataBase

    _preProcessedDataRepository = PreProcessedDataRepository()
    
    def __init__(self):
        super().__init__()

    