class Detection():
    def __init__(self,
        name,
        obfuscation,
        _type,
        obfuscationDegree,
        isGiven,
        isDetected,
        rawTextSuspiciousLocation,
        rawTextSourceLocation,
        textCollectionMeta,
        rawTextPair):
        self.name = name
        self.obfuscation = obfuscation
        self._type = _type
        self.obfuscationDegree = obfuscationDegree
        self.isGiven = isGiven
        self.isDetected = isDetected
        self.rawTextSuspiciousLocation = rawTextSuspiciousLocation
        self.rawTextSourceLocation = rawTextSourceLocation
        self.textCollectionMeta = textCollectionMeta
        self.rawTextPair = rawTextPair

