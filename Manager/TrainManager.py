import Process.LogProcess
import Process.PreProcessingRawTextProcess
import Process.SeedAttributesProcess
import Process.PlagiarismTypeProcess
import Process.SeedClassifierProcess

class TrainManager(object):

    def Hello(self):
        print ('Hello, I\'m the TrainManager')
        print ('And I manage these processes:')
        self._logProcess.Hello()
        self._preProcessingRawTextProcess.Hello()
        self._seedAttributesProcess.Hello()
        self._plagiarismTypeProcess.Hello()
        self._seedClassifierProcess.Hello()

    _logProcess = Process.LogProcess
    _preProcessingRawTextProcess = Process.PreProcessingRawTextProcess
    _seedAttributesProcess = Process.SeedAttributesProcess
    _plagiarismTypeProcess = Process.PlagiarismTypeProcess
    _seedClassifierProcess = Process.SeedClassifierProcess

    def __init__(self):
        pass

    
    