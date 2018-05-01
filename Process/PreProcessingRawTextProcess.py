from Internal import _TokenInternalProcess as TokenInternalProcess
from Internal import _RawTextInternalProcess as RawTextInternalProcess
from Process import _BaseProcess as BaseProcess

class PreProcessingRawTextProcess(BaseProcess):

    def Hello(self):
        self.logger.info('Testing from PreProcessingRawTextProcess')
        print ('Hello, I\'m the PreProcessingRawTextProcess')
        print ('And I use these repositories:')
        print ('And I use these internals:')
        self._tokenInternalProcess.Hello()
        self._rawTextInternalProcess.Hello()

    _tokenInternalProcess = TokenInternalProcess()
    _rawTextInternalProcess = RawTextInternalProcess()

    def __init__(self):
        super().__init__()

    