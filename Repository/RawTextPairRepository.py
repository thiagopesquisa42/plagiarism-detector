from Repository import _DataBaseConnection as DataBaseConnection
from Entity import _RawTextPair as RawTextPair

class RawTextPairRepository(DataBaseConnection):

    def Insert(self, rawTextPair):
        if(rawTextPair == None):
            return
        self.session.add(rawTextPair)
        self.session.commit()

    def Get(self, id):
        return self.session.query(RawTextPair).filter(RawTextPair.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
