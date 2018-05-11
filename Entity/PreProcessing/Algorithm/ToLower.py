from Entity.PreProcessing.Algorithm import _AbcAlgorithm as AbcAlgorithm
from Entity.PreProcessing.Algorithm import _AlgorithmClasses as AlgorithmClasses

class ToLower(AbcAlgorithm):
    def ToDictionary(self):
        return {
            'class': self._class,
            'description': self.description
        }

    def __init__(self, description = None):
        self._class = AlgorithmClasses.TO_LOWER
        self.description = description

