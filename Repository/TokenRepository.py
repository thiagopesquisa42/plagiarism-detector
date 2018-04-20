from Repository import _DataBaseConnection as DataBaseConnection
from Entity import _Token as Token

class TokenRepository(DataBaseConnection):

    def Insert(self, token):
        if(token == None):
            return
        self.session.add(token)
        self.session.commit()

    def Get(self, id):
        return self.session.query(Token).filter(Token.id == id).first()

    def Update(self, token):
        if(token == None):
            return
        tokenToUpdate = self.Get(token.id)
        tokenToUpdate.occurence = token.occurence + 5
        tokenToUpdate.text = token.text
        self.session.commit()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
