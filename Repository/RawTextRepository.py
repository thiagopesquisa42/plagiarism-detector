from Repository import _DataBaseConnection as DataBaseConnection
from Entity import _RawText as RawText

class RawTextRepository(DataBaseConnection):

    def Insert(self, rawText):
        if(rawText == None):
            return
        self.session.add(rawText)
        self.session.commit()
    
    def InsertList(self, rawTextList):
        if(rawTextList == None or len(rawTextList) == 0):
            return
        for rawText in rawTextList:
            self.session.add(rawText)
        self.session.commit()

    def Get(self, id):
        return self.session.query(RawText).filter(RawText.id == id).first()

    def GetTupleRawTextIdsSuspiciousSource(self, tupleFileNameSuspiciousSource, textCollectionMetaId):
        rawTextSuspiciousId = self.session.query(RawText.id).filter(
            (RawText.fileName == tupleFileNameSuspiciousSource[0]) & 
            (RawText.textCollectionMetaId == textCollectionMetaId)).scalar()
        rawTextSourceId = self.session.query(RawText.id).filter(
            (RawText.fileName == tupleFileNameSuspiciousSource[1]) & 
            (RawText.textCollectionMetaId == textCollectionMetaId)).scalar()
        if((rawTextSuspiciousId is not None)
            and (rawTextSourceId is not None)):
            return (rawTextSuspiciousId, rawTextSourceId)
        else:
            return None

    # def Update(self, rawText):
    #     if(rawText == None):
    #         return
    #     rawTextToUpdate = self.Get(rawText.id)
    #     rawTextToUpdate.fileName = rawText.fileName
    #     rawTextToUpdate._type = rawText._type
    #     rawTextToUpdate.text = rawText.text
    #     self.session.commit()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()