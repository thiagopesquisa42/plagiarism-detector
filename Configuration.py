def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class ConstantsConfigurations(object):
    @constant
    def DATA_BASE_NAME():
        return "PlagiarismDetection"
    @constant
    def DATA_BASE_PASSWORD():
        return "123456"
    @constant
    def DATA_BASE_USER():
        return "user"

CONSTANTS_CONFIGURATIONS = ConstantsConfigurations()

def Hello():
    print("Testing Configuration Accessor:")
    print("DataBaseName: ",CONSTANTS_CONFIGURATIONS.DATA_BASE_NAME)

    
