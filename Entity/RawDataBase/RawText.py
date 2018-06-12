class RawText():
    def __init__(self,
        text,
        fileName,
        _type,
        textCollectionMeta):
        self.text = text
        self.fileName = fileName
        self._type = _type
        self.textCollectionMeta = textCollectionMeta

    def GetRawTextNumber(self):
        return self.fileName.split('.')[0].split('document')[1]
