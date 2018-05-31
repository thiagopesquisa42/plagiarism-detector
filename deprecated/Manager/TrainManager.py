from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess

class TrainManager(object):

    def Hello(self):
        print ('Hello, I\'m the TrainManager')
        print ('And I manage these processes:')
        self._preProcessingRawTextProcess.Hello()
    
    _preProcessingRawTextProcess = PreProcessingRawTextProcess()

    def __init__(self):
        pass

    
    