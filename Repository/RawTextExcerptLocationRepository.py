from Repository import _DataBaseConnection as DataBaseConnection
from Entity import _RawTextExcerptLocation as RawTextExcerptLocation

class RawTextExcerptLocationRepository(DataBaseConnection):

    def Insert(self, rawTextExcerptLocation):
        if(rawTextExcerptLocation == None):
            return
        self.session.add(rawTextExcerptLocation)
        self.session.commit()

    def Get(self, id):
        return self.session.query(RawTextExcerptLocation).filter(RawTextExcerptLocation.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
