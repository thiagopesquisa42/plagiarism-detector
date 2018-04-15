import Manager.TrainManager
import Manager.TestManager

def Hello():
    print ('Hello, I\'m the CrossValidationView')
    print ('And I depends of that guy(s):')
    Manager.TrainManager.Hello()
    Manager.TestManager.Hello()