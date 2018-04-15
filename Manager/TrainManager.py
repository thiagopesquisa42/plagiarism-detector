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

    _logProcess = Process.LogProcess.LogProcess()
    _preProcessingRawTextProcess = Process.PreProcessingRawTextProcess.PreProcessingRawTextProcess()
    _seedAttributesProcess = Process.SeedAttributesProcess.SeedAttributesProcess()
    _plagiarismTypeProcess = Process.PlagiarismTypeProcess.PlagiarismTypeProcess()
    _seedClassifierProcess = Process.SeedClassifierProcess.SeedClassifierProcess()

    def __init__(self):
        pass

    
    