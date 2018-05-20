from Repository import _BaseRepository as BaseRepository
from Entity import _RawText as RawText

class RawTextRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(RawText).filter(RawText.id == id).first()
    
    def GetByTextCollectionMetaId(self, textCollectionMetaId):
        return self.session.query(RawText).filter(RawText.textCollectionMetaId == textCollectionMetaId).all()

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

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()