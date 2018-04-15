import Process.LogProcess
import Process.PreProcessingRawTextProcess
import Process.SeedAttributesProcess
import Process.SeedEvaluationProcess

class TestManager(object):

    def Hello(self):
        print ('Hello, I\'m the TestManager')
        print ('And I manage these processes:')
        self._logProcess.Hello()
        self._preProcessingRawTextProcess.Hello()
        self._seedAttributesProcess.Hello()
        self._seedEvaluationProcess.Hello()

    _logProcess = Process.LogProcess
    _preProcessingRawTextProcess = Process.PreProcessingRawTextProcess
    _seedAttributesProcess = Process.SeedAttributesProcess
    _seedEvaluationProcess = Process.SeedEvaluationProcess

    def __init__(self):
        pass

    
