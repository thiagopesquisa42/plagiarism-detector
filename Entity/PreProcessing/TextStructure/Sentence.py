
class Sentence():
    def __init__(self,
        text,
        rawTextExcerptLocation,
        bagOfWords = None,
        nGramsList = None):
        self.text = text 
        self.rawTextExcerptLocation = rawTextExcerptLocation 
        self.bagOfWords = bagOfWords 
        self.nGramsList = nGramsList 
