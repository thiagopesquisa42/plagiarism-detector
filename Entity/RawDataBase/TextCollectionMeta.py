
class TextCollectionMeta():
    def __init__(self,
        creationDate,
        name,
        sourceUrl,
        description,
        textCollectionMetaPurpose):
        self.creationDate = creationDate
        self.name  = name 
        self.sourceUrl = sourceUrl
        self.description = description
        self.purpose = textCollectionMetaPurpose
        self.testTextCollectionMeta = None
        self.rawTextList = []
        self.rawTextPairList = []
        self.detectionList = []

