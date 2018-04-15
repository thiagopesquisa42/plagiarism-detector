import Manager.TrainManager
import Manager.TestManager

def Hello():
    print ('Hello, I\'m the CrossValidationView')
    print ('And I shows the output of these managers:')
    Manager.TrainManager.Hello()
    Manager.TestManager.Hello()