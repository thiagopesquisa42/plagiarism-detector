from Process import _SetupProcess as SetupProcess
from Process import _LogProcess as LogProcess

class SetupManager(object):

    def Hello(self):
        print ('Hello, I\'m the SetupManager')
        print ('And I manage these processes:')
        self._setupProcess.Hello()
        self._logProcess.Hello()

    _setupProcess = SetupProcess()
    _logProcess = LogProcess()

    def __init__(self):
        pass
