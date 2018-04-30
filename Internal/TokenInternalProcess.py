from Entity import _Token as Token
from Repository import _TokenRepository as TokenRepository

class TokenInternalProcess(object):

    def Hello(self):
        print ('Hello, I\'m the TokenInternalProcess')
        print ('And I use these repositories:')
        self._tokenRepository.Hello()
        
        token = Token()
        token.text = 'Teste 3 testando... oioioioioi 20180416'
        token.occurence = 1
        self._tokenRepository.Insert(token)
        token = self._tokenRepository.Get(id = 345645)
        self._tokenRepository.Update(token)

    _tokenRepository = TokenRepository()

    def __init__(self):
        pass
