from Repository import _DataBaseConnection as DataBaseConnection
from Entity import _TextCollectionMeta as TextCollectionMeta

class TextCollectionMetaRepository(DataBaseConnection):

    def Insert(self, textCollectionMeta):
        if(textCollectionMeta == None):
            return
        self.session.add(textCollectionMeta)
        self.session.commit()
        return textCollectionMeta.id

    def Get(self, id):
        return self.session.query(TextCollectionMeta).filter(TextCollectionMeta.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
