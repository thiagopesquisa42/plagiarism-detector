from Repository import _DataBaseConnection as DataBaseConnection
from Entity import _RawText as RawText

class RawTextRepository(DataBaseConnection):

    def Insert(self, rawText):
        if(rawText == None):
            return
        self.session.add(rawText)
        self.session.commit()

    def Get(self, id):
        return self.session.query(RawText).filter(RawText.id == id).first()

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