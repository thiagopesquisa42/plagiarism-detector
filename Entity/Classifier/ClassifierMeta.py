
class ClassifierMeta():
    def __init__(self,
        classifier,
        definitionDictionary):
        self.classifier = classifier
        self.definitionDictionary = definitionDictionary
        self.summaryTestData = None
        self.summaryTrainData = None
        self.expectedPredictedList = None
        self.report = None
        self.graphviz = None
