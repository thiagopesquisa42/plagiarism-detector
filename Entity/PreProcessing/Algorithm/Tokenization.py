from Entity.PreProcessing.Algorithm import _AbcAlgorithm as AbcAlgorithm
from Entity.PreProcessing.Algorithm import _AlgorithmClasses as AlgorithmClasses

class Tokenization(AbcAlgorithm):
    def ToDictionary(self):
        return {
            'class': self._class,
            'type': self._type,
            'algorithm': self.algorithm,
            'description': self.description
        }

    def __init__(self, _type, algorithm, description = None):
        self._class = AlgorithmClasses.TOKENIZATION
        self._type = _type
        self.algorithm = algorithm
        self.description = description

class TokenizationType():
    SENTENCE = 'sentence tokenizer'
    WORD = 'word tokenizer'

class TokenizationAlgorithm():
    PUNKT_EN = 'punkt english'
    TREEBANK_WORD_TOKENIZER = 'treebank word tokenizer'
