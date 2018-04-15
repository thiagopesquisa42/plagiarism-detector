import Process.SetupProcess
import Process.LogProcess

class SetupManager(object):

    def __init__(self):
        pass

    def Hello(self):
        print ('Hello, I\'m the SetupManager')
        print ('And I manage these processes:')
        Process.SetupProcess.Hello()
        Process.LogProcess.Hello()
