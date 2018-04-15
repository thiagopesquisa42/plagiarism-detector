import Process.SetupProcess
import Process.LogProcess

def Hello():
    print ('Hello, I\'m the SetupManager')
    print ('And I manage these processes:')
    Process.SetupProcess.Hello()
    Process.LogProcess.Hello()
