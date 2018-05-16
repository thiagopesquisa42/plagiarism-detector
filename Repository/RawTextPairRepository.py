from Repository import _BaseRepository as BaseRepository
from Entity import _RawTextPair as RawTextPair
from Entity import _RawText as RawText
from sqlalchemy import or_

class RawTextPairRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(RawTextPair).filter(RawTextPair.id == id).first()

    def GetListByTextCollectionMeta(self, textCollectionMeta):
        return self.session.query(RawTextPair).\
            join((RawText, RawTextPair.sourceRawTextId == RawText.id)).\
            filter(RawText.textCollectionMeta == textCollectionMeta).\
            all()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
