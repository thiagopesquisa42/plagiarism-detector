def setLogger():
    init = "Log register: \n"
    asctime = "\tasctime: %(asctime)s \n";
    filename = "\tfilename: %(filename)s \n";
    funcName = "\tfuncName: %(funcName)s \n";
    levelname = "\tlevelname: %(levelname)s \n";
    lineno = "\tlineno: %(lineno)d \n";
    module = "\tmodule: %(module)s \n";
    message = "\tmessage: %(message)s \n";
    name = "\tname: %(name)s \n";
    pathname = "\tpathname: %(pathname)s \n";

    logFormat = init + asctime + filename + funcName + levelname + lineno + module + message + name + pathname      
    logging.basicConfig(filename = 'logging.sqlalchemy.log',
                        level = logging.DEBUG,
                        format = logFormat)
    logging.getLogger(name = 'sqlalchemy.engine').setLevel(logging.DEBUG)