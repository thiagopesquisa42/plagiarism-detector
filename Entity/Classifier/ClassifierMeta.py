
class ClassifierMeta():
    def __init__(self,
        classifier,
        definitionDictionary):
        self.classifier = classifier
        self.definitionDictionary = definitionDictionary
        self.expectedPredictedList = None
        self.report = None
        self.graphviz = None
