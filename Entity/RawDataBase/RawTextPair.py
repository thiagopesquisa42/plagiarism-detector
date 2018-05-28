
class RawTextPair():
    def __init__(self,
        sourceRawText,
        suspiciousRawText):
        self.sourceRawText = sourceRawText
        self.suspiciousRawText = suspiciousRawText
    
    @staticmethod
    def isEqual(left, right):
        return left.suspiciousRawText.fileName == right.suspiciousRawText.fileName and\
            left.sourceRawText.fileName == right.sourceRawText.fileName