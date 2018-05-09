from Repository import _DataBaseConnection as DataBaseConnection
from Entity.PreProcessing.Bag import _Text as Text

class TextRepository(DataBaseConnection):

    def Insert(self, text):
        if(text == None):
            return
        self.session.add(text)
        self.session.commit()
    
    def InsertList(self, textList):
        if(textList == None or len(textList) == 0):
            return
        for text in textList:
            self.session.add(text)
        self.session.commit()

    def Get(self, id):
        return self.session.query(Text).filter(Text.id == id).first()
    
    def GetByBagOfTextsId(self, bagOfTextsId):
        return self.session.query(Text).filter(Text.bagOfTextsId == bagOfTextsId).all()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()