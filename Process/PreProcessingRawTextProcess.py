from Internal import _RawTextInternalProcess as RawTextInternalProcess
from Process import _BaseProcess as BaseProcess
from Entity import _BagOfTexts as BagOfTexts
import nltk

class PreProcessingRawTextProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from PreProcessingRawTextProcess')
        print ('Hello, I\'m the PreProcessingRawTextProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')
        self._rawTextInternalProcess.Hello()

    def PreProcessing(self, textCollectionMetaId):
        rawTextList = self._rawTextInternalProcess.GetRawTextsByCollectionId(textCollectionMetaId)
        a = BagOfTexts()
        print('')



    def LowerRawTextList(rawTextList):
        pass

    def LowerRawText(rawText):
        return rawText.text.lower()
        

        # nltk....
        pass

    _rawTextInternalProcess = RawTextInternalProcess()

    def __init__(self):
        super().__init__()

    