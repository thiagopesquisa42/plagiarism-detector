from abc import ABC, abstractmethod
 
class AbcAlgorithm(ABC):
    @abstractmethod
    def ToDictionary(self):
        #the inherited classes has to provides a cast to Dictionary type
        pass

    def __init__(self):
        super().__init__()

class AlgorithmClasses():
    TOKENIZATION = 'tokenization'
    TO_LOWER = 'to lower'
    REMOVE_STOPWORDS = 'remove stopwords'   
    FUSE_SENTENCES = 'fuse sentences'
    STEMMING = 'stemming'
    LEMMATIZATION = 'lemmatization'
    N_GRAMS_GENERATOR = 'n-grams generator'

