from Entity.PreProcessing.Algorithm import _AbcAlgorithm as AbcAlgorithm
from Entity.PreProcessing.Algorithm import _AlgorithmClasses as AlgorithmClasses

class Stemmer(AbcAlgorithm):
    def ToDictionary(self):
        return {
            'class': self._class,
            'algorithm': self.algorithm,
            'description': self.description
        }

    def __init__(self, algorithm, description = None):
        self._class = AlgorithmClasses.STEMMING
        self.algorithm = algorithm
        self.description = description

class StemmerAlgorithm():
    PORTER = 'porter english'
