import Manager.TrainManager
import Manager.TestManager

class CrossValidationView(object):

    def Hello(self):
        print ('Hello, I\'m the CrossValidationView')
        print ('And I shows the output of these managers:')
        self._trainManager.Hello()
        self._testManager.Hello()

    _testManager = Manager.TestManager
    _trainManager = Manager.TrainManager

    def __init__(self):
        pass
