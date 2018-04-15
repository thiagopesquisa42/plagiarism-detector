import Process.LogProcess
import Process.PreProcessingRawTextProcess
import Process.SeedAttributesProcess
import Process.SeedEvaluationProcess

def Hello():
    print ('Hello, I\'m the TestManager')
    print ('And I manage these processes:')
    Process.LogProcess.Hello()
    Process.PreProcessingRawTextProcess.Hello()
    Process.SeedAttributesProcess.Hello()
    Process.SeedEvaluationProcess.Hello()
    
