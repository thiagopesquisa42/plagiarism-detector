from Internal import _TokenInternalProcess as TokenInternalProcess
from Internal import _RawTextInternalProcess as RawTextInternalProcess

class PreProcessingRawTextProcess(object):

    def Hello(self):
        print ('Hello, I\'m the PreProcessingRawTextProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')
        self._tokenInternalProcess.Hello()
        self._rawTextInternalProcess.Hello()
        self._rawTextInternalProcess.TestInsertARawText()

    _tokenInternalProcess = TokenInternalProcess()
    _rawTextInternalProcess = RawTextInternalProcess()

    def __init__(self):
        pass

    