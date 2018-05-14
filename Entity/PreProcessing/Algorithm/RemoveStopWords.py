from Entity.PreProcessing.Algorithm import _AbcAlgorithm as AbcAlgorithm
from Entity.PreProcessing.Algorithm import _AlgorithmClasses as AlgorithmClasses

class RemoveStopWords(AbcAlgorithm):
    def ToDictionary(self):
        return {
            'class': self._class,
            'stopWordList': self.stopWordList,
            'description': self.description
        }

    def __init__(self, stopWordList, description = None):
        self._class = AlgorithmClasses.REMOVE_STOPWORDS
        self.stopWordList = stopWordList
        self.description = description

