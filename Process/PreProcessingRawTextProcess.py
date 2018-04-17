import Internal.TokenInternalProcess
import Internal.RawTextInternalProcess

class PreProcessingRawTextProcess(object):

    def Hello(self):
        print ('Hello, I\'m the PreProcessingRawTextProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')
        self._tokenInternalProcess.Hello()
        self._rawTextInternalProcess.Hello()
        self._rawTextInternalProcess.TestInsertARawText()

    _tokenInternalProcess = Internal.TokenInternalProcess.TokenInternalProcess()
    _rawTextInternalProcess = Internal.RawTextInternalProcess.RawTextInternalProcess()

    def __init__(self):
        pass

    