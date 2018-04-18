from Manager import _TrainManager as TrainManager
from Manager import _TestManager as TestManager

class CrossValidationView(object):

    def Hello(self):
        print ('Hello, I\'m the CrossValidationView')
        print ('And I shows the output of these managers:')
        self._trainManager.Hello()
        self._testManager.Hello()

    _testManager = TestManager()
    _trainManager = TrainManager()

    def __init__(self):
        pass
