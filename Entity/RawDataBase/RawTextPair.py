from functools import total_ordering

@total_ordering
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

    def __lt__(self, other):
        return self.suspiciousRawText.GetRawTextNumber() < other.suspiciousRawText.GetRawTextNumber() or \
            (self.suspiciousRawText.GetRawTextNumber() == other.suspiciousRawText.GetRawTextNumber() and \
            self.sourceRawText.GetRawTextNumber() < other.sourceRawText.GetRawTextNumber())
    
    