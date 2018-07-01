
class ClassifierMeta():
    def __init__(self,
        classifier,
        definitionDictionary, nickname = 'CLASSIFIER'):
        self.classifier = classifier
        self.definitionDictionary = definitionDictionary if(self.AcceptDefinitionDictionary(definitionDictionary)) else None
        self.summaryTrainData = None
        self.attributesReport = None
        self.summaryTestData = None
        self.metaDataFrame = None
        self.report = None
        self.graphviz = None

    def AcceptDefinitionDictionary(self, definitionDictionary):
        if('name' not in definitionDictionary.keys()):
            raise Exception('definitionDictionary must have a name propertie!')
        return True

    def GetName(self):
        return self.definitionDictionary['name'].replace(" ", "")