import Manager.TrainManager

class ExecuteView(object):

    def Hello(self):
        print ('Hello, I\'m the ExecuteView')
        print ('And I shows the output of these managers:')
        self._trainManager.Hello()

    _trainManager = Manager.TrainManager.TrainManager()

    def __init__(self):
        pass
