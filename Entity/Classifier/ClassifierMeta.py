
class ClassifierMeta():
    def __init__(self,
        classifier,
        definitionDictionary):
        self.classifier = classifier
        self.definitionDictionary = definitionDictionary
        self.summaryTrainData = None
        self.attributesReport = None
        self.summaryTestData = None
        self.metaDataFrame = None
        self.report = None
        self.graphviz = None
