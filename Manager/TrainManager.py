import Process.LogProcess
import Process.PreProcessingRawTextProcess
import Process.SeedAttributesProcess
import Process.PlagiarismTypeProcess
import Process.SeedClassifierProcess

def Hello():
    print ('Hello, I\'m the TrainManager')
    print ('And I manage these processes:')
    Process.LogProcess.Hello()
    Process.PreProcessingRawTextProcess.Hello()
    Process.SeedAttributesProcess.Hello()
    Process.PlagiarismTypeProcess.Hello()
    Process.SeedClassifierProcess.Hello()    
    