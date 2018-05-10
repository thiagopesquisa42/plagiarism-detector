from Repository import _BaseRepository as BaseRepository
from Entity.PreProcessing import _RawTextExcerptLocation as RawTextExcerptLocation
from Entity import _RawText as RawText

class RawTextExcerptLocationRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(RawTextExcerptLocation).filter(RawTextExcerptLocation.id == id).first()

    def GetAllFromTextCollectionMetaId(self, textCollectionMetaId):
        return self.session.query(
            RawTextExcerptLocation).join(
                RawText).filter(
                    RawText.textCollectionMetaId == textCollectionMetaId).all()
        
    def GetIdByRawTextIdLengthFirstCharacter(self, rawTextId, stringLength, firstCharacterPosition):
        rawTextExcerptLocationId = self.session.query(RawTextExcerptLocation.id).filter(
            (RawTextExcerptLocation.rawTextId == rawTextId) & 
            (RawTextExcerptLocation.stringLength == stringLength) &
            (RawTextExcerptLocation.firstCharacterPosition == firstCharacterPosition)).one_or_none()
        return rawTextExcerptLocationId
    
    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
