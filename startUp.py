from View import _SetupView as SetupView
from View import _ExecuteView as ExecuteView
from View import _ValidationView as ValidationView
from View import _CrossValidationView as CrossValidationView

class StartUp(object):

    def Hello(self):
        print('Hello, I\'m StartUp and I\'m the top guy, who sets up everbody!')

    def LayersComunnicationTest(self):
        self.Hello()
        self._setupView.Hello()
        self._executeView.Hello()
        self._validationView.Hello()
        self._crossValidationView.Hello()

    _setupView = SetupView()
    _executeView = ExecuteView()
    _validationView = ValidationView()
    _crossValidationView = CrossValidationView()

    def __init__(self):
        pass

StartUp().LayersComunnicationTest()
