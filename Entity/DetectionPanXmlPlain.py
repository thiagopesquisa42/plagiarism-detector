
class DetectionPanXmlPlain():
    def __init__(self, name, obfuscation, obfuscationDegree, _type, suspiciousFileName,
        suspiciousLength, suspiciousOffset, sourceLength, sourceOffset, sourceFileName):
        self.name = name
        self.obfuscation = obfuscation
        self.obfuscationDegree = obfuscationDegree
        self._type = _type
        self.suspiciousFileName = suspiciousFileName
        self.suspiciousLength = suspiciousLength
        self.suspiciousOffset = suspiciousOffset
        self.sourceLength = sourceLength
        self.sourceOffset = sourceOffset
        self.sourceFileName = sourceFileName

