from Entity import _TextCollectionMeta as TextCollectionMeta
from Entity import _RawText as RawText
from Entity import _RawTextType as RawTextType
from Repository import _TextCollectionMetaRepository as TextCollectionMetaRepository
from Repository import _RawTextRepository as RawTextRepository

class DataImportationProcess(object):

    def Hello(self):
        print ('Hello, I\'m the DataImportationProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')
        self._tokenInternalProcess.Hello()
        self._rawTextInternalProcess.Hello()
        self._rawTextInternalProcess.TestInsertARawText()

    def ImportFromPanFiles(self, folderCompletePath, dataBaseCreationDate):
        tcm = TextCollectionMeta(creationDate = '2014-05-14', description = 'pan14-text-alignment-test-corpus3-2014-05-14', sourceUrl = None, name = 'base do Pan 2014')        
        self._textCollectionMetaRepository.Insert(textCollectionMeta = tcm)
        rt = RawText(_type = RawTextType.suspicious, 
                    textCollectionMetaId = tcm.id,
                    text = 'Este é um texto de teste!!',
                    fileName = 'text/random/susp00043.txt')
        self._rawTextRepository.Insert(rawText = rt)
        rt2 = self._rawTextRepository.Get(id = rt.id)
        print(rt2.id, rt2.textCollectionMetaId, rt2.text, rt2.fileName, rt2.textCollectionMeta.name)
        
    _textCollectionMetaRepository = TextCollectionMetaRepository()
    _rawTextRepository = RawTextRepository()

    def __init__(self):
        pass