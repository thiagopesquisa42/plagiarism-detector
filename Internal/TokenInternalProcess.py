from Entity import _Token as Token
from Repository import _TokenRepository as TokenRepository

class TokenInternalProcess(object):

    def Hello(self):
        print ('Hello, I\'m the TokenInternalProcess')
        print ('And I use these repositories:')
        self._tokenRepository.Hello()

    _tokenRepository = TokenRepository()

    def __init__(self):
        pass

