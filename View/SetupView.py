from Manager import _SetupManager as SetupManager

class SetupView(object):

    def Hello(self):
        print ('Hello, I\'m the SetupView')
        print ('And I shows the output of these managers:')
        self._setupManager.Hello()

    _setupManager = SetupManager()

    def __init__(self):
        pass
