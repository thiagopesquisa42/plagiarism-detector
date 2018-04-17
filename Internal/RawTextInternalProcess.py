from Entity import _RawText as RawText
from Entity import _RawTextType as RawTextType
import Repository.RawTextRepository

class RawTextInternalProcess(object):
    def TestInsertARawText(self):
        document = RawText(
            text="iadnvlkjnadhm j dofm d  fdscfcs fvofmcs df ", 
            fileName = 'suspicious0001.txt', 
            _type = RawTextType.suspicious)
        self._rawTextRepository.Insert(document)

    def Hello(self):
        print ('Hello, I\'m the RawTextInternalProcess')
        print ('And I use these repositories:')

    _rawTextRepository = Repository.RawTextRepository.RawTextRepository()

    def __init__(self):
        pass

