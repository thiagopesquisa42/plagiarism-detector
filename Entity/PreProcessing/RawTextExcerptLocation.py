class RawTextExcerptLocation():
    def __init__(self,
        firstCharacterPosition,
        lastCharacterPosition,
        stringLength,
        rawText):
        self.firstCharacterPosition = firstCharacterPosition
        self.lastCharacterPosition = lastCharacterPosition
        self.stringLength = stringLength
        self.rawText = rawText
