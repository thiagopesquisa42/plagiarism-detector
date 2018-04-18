from Process import _LogProcess as LogProcess
from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess
from Process import _SeedAttributesProcess as SeedAttributesProcess
from Process import _SeedEvaluationProcess as SeedEvaluationProcess

class TestManager(object):

    def Hello(self):
        print ('Hello, I\'m the TestManager')
        print ('And I manage these processes:')
        self._logProcess.Hello()
        self._preProcessingRawTextProcess.Hello()
        self._seedAttributesProcess.Hello()
        self._seedEvaluationProcess.Hello()

    _logProcess = LogProcess()
    _preProcessingRawTextProcess = PreProcessingRawTextProcess()
    _seedAttributesProcess = SeedAttributesProcess()
    _seedEvaluationProcess = SeedEvaluationProcess()

    def __init__(self):
        pass

    
