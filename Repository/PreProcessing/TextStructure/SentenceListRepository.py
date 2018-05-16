from Repository import _BaseRepository as BaseRepository
from Entity.PreProcessing.TextStructure import _SentenceList as SentenceList
from Entity.PreProcessing import _RawTextExcerptLocation as RawTextExcerptLocation

class SentenceListRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(SentenceList).filter(SentenceList.id == id).first()
    
    def GetByPreProcessStepChainNode(self, preProcessStepChainNode):
        return self.session.query(SentenceList).\
            filter(SentenceList.preProcessStepChainNode == preProcessStepChainNode).all()
    
    def GetByRawText(self, rawText, preProcessedData):
        return self.session.query(SentenceList).\
            filter(SentenceList.rawText == rawText).\
            one()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
