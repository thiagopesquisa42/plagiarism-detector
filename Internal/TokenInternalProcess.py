import Repository.TokenRepository
from Entity.Token import Token

class TokenInternalProcess(object):

    def Hello(self):
        print ('Hello, I\'m the TokenInternalProcess')
        print ('And I use these repositories:')
        self._tokenRepository.Hello()
        
        token = Token()
        token.text = 'Teste 2 testando... Ç^Ç`^Ç^#$@#$@R$¨&¨ÀÀ`\'`^^`^`^``'
        token.occurence = 1
        self._tokenRepository.Insert(token)
        token = self._tokenRepository.Get(id = 345645)
        self._tokenRepository.Update(token)

    _tokenRepository = Repository.TokenRepository.TokenRepository()

    def __init__(self):
        pass

