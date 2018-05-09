from Internal import _RawTextInternalProcess as RawTextInternalProcess
from Process import _BaseProcess as BaseProcess
from Repository.PreProcessing.Bag import _BagOfTextsRepository as BagOfTextsRepository
from Repository.PreProcessing.Bag import _TextRepository as TextRepository
from Repository import _RawTextExcerptLocationRepository as RawTextExcerptLocationRepository
from Entity.PreProcessing.Bag import _BagOfTexts as BagOfTexts
from Entity.PreProcessing.Bag import _BagOfTexts as BagOfTexts
from Entity.PreProcessing.Bag import _Text as Text
from Entity.PreProcessing import _RawTextExcerptLocation as RawTextExcerptLocation

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
            rawTextList = self._rawTextInternalProcess.GetRawTextsByCollectionId(textCollectionMetaId)
            bagOfTexts = self.CreateGetBagOfTextsLowered(rawTextList)
        except Exception as exception:
            self.logger.info('PreProcessing failure: ' + str(exception))
        else:
            self.logger.info('PreProcessing finished')

    def CreateGetBagOfTextsLowered(self, rawTextList):
        if(rawTextList is None or len(rawTextList) == 0):
            return None
        textCollectionMetaId = rawTextList[0].textCollectionMetaId
        bagOfTexts = BagOfTexts(textCollectionMetaId = textCollectionMetaId)
        textList = []
        for rawText in rawTextList:
            loweredText = self.LowerRawText(rawText)
            rawTextExcerptLocation = RawTextExcerptLocation(
                rawTextId = rawText.id,
                stringLength = len(rawText.text),
                firstCharacterPosition = 0)
            text = Text(
                text = loweredText,
                rawTextExcerptLocation = rawTextExcerptLocation,
                bagOfTexts = bagOfTexts)
            textList.append(text)
        self._textRepository.InsertList(textList)
        return bagOfTexts
            

    def LowerRawText(self, rawText):
        return rawText.text.lower()

    _rawTextInternalProcess = RawTextInternalProcess()
    _bagOfTextsRepository = BagOfTextsRepository()
    _textRepository = TextRepository()
    _rawTextExcerptLocationRepository = RawTextExcerptLocationRepository()

    def __init__(self):
        super().__init__()

    