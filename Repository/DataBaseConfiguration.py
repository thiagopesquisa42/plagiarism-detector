def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class ConstantsConfigurations(object):
    @constant
    def DATA_BASE_NAME():
        return "plagiarism_detection"
    @constant
    def DATA_BASE_PASSWORD():
        return "1234"
    @constant
    def DATA_BASE_USER():
        return "root"
    @constant
    def DATA_BASE_HOST():
        return "localhost"
    @constant
    def DATA_BASE_PORT():
        return "3306"
    @constant
    def SQLALCHEMY_CONNECTION_STRING_DATA_BASE():
        #'mysql+pymysql://user:password@host:port/dbName'
        _self = ConstantsConfigurations()
        sgbd = 'mysql'
        protocol = 'pymysql'
        user = _self.DATA_BASE_USER
        password = _self.DATA_BASE_PASSWORD
        host = _self.DATA_BASE_HOST
        port = _self.DATA_BASE_PORT
        dataBaseName = _self.DATA_BASE_NAME
        connectionString = sgbd + '+' + protocol + '://' + user + ':' + password + '@' + host + ':' + port + '/' + dataBaseName
        return connectionString

CONSTANTS_CONFIGURATIONS = ConstantsConfigurations()

    
