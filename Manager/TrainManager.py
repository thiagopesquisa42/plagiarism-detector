from Process import _LogProcess as LogProcess
from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess
from Process import _SeedAttributesProcess as SeedAttributesProcess
from Process import _PlagiarismTypeProcess as PlagiarismTypeProcess
from Process import _SeedClassifierProcess as SeedClassifierProcess

class TrainManager(object):

    def Hello(self):
        print ('Hello, I\'m the TrainManager')
        print ('And I manage these processes:')
        self._logProcess.Hello()
        self._preProcessingRawTextProcess.Hello()
        self._seedAttributesProcess.Hello()
        self._plagiarismTypeProcess.Hello()
        self._seedClassifierProcess.Hello()

    _logProcess = LogProcess()
    _preProcessingRawTextProcess = PreProcessingRawTextProcess()
    _seedAttributesProcess = SeedAttributesProcess()
    _plagiarismTypeProcess = PlagiarismTypeProcess()
    _seedClassifierProcess = SeedClassifierProcess()

    def __init__(self):
        pass

    
    