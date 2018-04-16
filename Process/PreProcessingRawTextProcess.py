import Internal.TokenInternalProcess

class PreProcessingRawTextProcess(object):

    def Hello(self):
        print ('Hello, I\'m the PreProcessingRawTextProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')
        self._tokenInternalProcess.Hello()

    _tokenInternalProcess = Internal.TokenInternalProcess.TokenInternalProcess()

    def __init__(self):
        pass

    