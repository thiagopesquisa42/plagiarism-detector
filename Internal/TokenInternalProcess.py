import Repository.TokenRepository

class TokenInternalProcess(object):

    def Hello(self):
        print ('Hello, I\'m the TokenInternalProcess')
        print ('And I use these repositories:')
        self._tokenRepository.Hello()

    _tokenRepository = Repository.TokenRepository

    def __init__(self):
        pass

