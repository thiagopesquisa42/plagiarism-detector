from Repository import _DataBaseConnection as DataBaseConnection
from Entity.PreProcessing.Bag import _BagOfTexts as BagOfTexts

class BagOfTextsRepository(DataBaseConnection):

    def Insert(self, bagOfTexts):
        if(bagOfTexts == None):
            return
        self.session.add(bagOfTexts)
        self.session.commit()
    
    def InsertList(self, bagOfTextsList):
        if(bagOfTextsList == None or len(bagOfTextsList) == 0):
            return
        for bagOfTexts in bagOfTextsList:
            self.session.add(bagOfTexts)
        self.session.commit()

    def Get(self, id):
        return self.session.query(BagOfTexts).filter(BagOfTexts.id == id).first()
    
    def GetByTextCollectionMetaId(self, textCollectionMetaId):
        return self.session.query(BagOfTexts).filter(BagOfTexts.textCollectionMetaId == textCollectionMetaId).all()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()