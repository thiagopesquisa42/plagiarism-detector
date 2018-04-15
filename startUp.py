import View.SetupView as SetupView
import View.ExecuteView as ExecuteView
import View.ValidationView as ValidationView
import View.CrossValidationView as CrossValidationView

def Hello():
    print('Hello, I\'m StartUp and I\'m the top guy, who sets up everbody!')

def LayersComunnicationTest():
    Hello()
    SetupView.Hello()
    ExecuteView.Hello()
    ValidationView.Hello()
    CrossValidationView.Hello()

LayersComunnicationTest()