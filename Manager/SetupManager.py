import Process.SetupProcess
import Process.LogProcess

class SetupManager(object):

    def Hello(self):
        print ('Hello, I\'m the SetupManager')
        print ('And I manage these processes:')
        self._setupProcess.Hello()
        self._logProcess.Hello()

    _setupProcess = Process.SetupProcess
    _logProcess = Process.LogProcess

    def __init__(self):
        pass
