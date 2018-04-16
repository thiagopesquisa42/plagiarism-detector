import View.SetupView
import View.ExecuteView
import View.ValidationView
import View.CrossValidationView

class StartUp(object):

    def Hello(self):
        print('Hello, I\'m StartUp and I\'m the top guy, who sets up everbody!')

    def LayersComunnicationTest(self):
        self.Hello()
        self._setupView.Hello()
        self._executeView.Hello()
        self._validationView.Hello()
        self._crossValidationView.Hello()

    _setupView = View.SetupView.SetupView()
    _executeView = View.ExecuteView.ExecuteView()
    _validationView = View.ValidationView.ValidationView()
    _crossValidationView = View.CrossValidationView.CrossValidationView()

    def __init__(self):
        pass

StartUp().LayersComunnicationTest()
