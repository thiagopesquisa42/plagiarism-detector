
class ClassifierMeta():
    def __init__(self,
        classifier,
        definitionDictionary):
        self.classifier = classifier
        self.definitionDictionary = definitionDictionary
        self.seedingDataFrame = None
        self.expectedPredictedList = None
