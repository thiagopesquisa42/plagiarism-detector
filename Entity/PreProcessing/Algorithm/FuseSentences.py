from Entity.PreProcessing.Algorithm import _AbcAlgorithm as AbcAlgorithm
from Entity.PreProcessing.Algorithm import _AlgorithmClasses as AlgorithmClasses

class FuseSentences(AbcAlgorithm):
    def ToDictionary(self):
        return {
            'class': self._class,
            'threshold': self.threshold,
            'description': self.description
        }

    def __init__(self, threshold, description = None):
        self._class = AlgorithmClasses.FUSE_SENTENCES
        self.threshold = threshold
        self.description = description

