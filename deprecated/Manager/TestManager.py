from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess

class TestManager(object):

    def Hello(self):
        print ('Hello, I\'m the TestManager')
        print ('And I manage these processes:')
        self._preProcessingRawTextProcess.Hello()

    _preProcessingRawTextProcess = PreProcessingRawTextProcess()

    def __init__(self):
        pass

    
