def GetLoggerFormat():
    init = "\n"
    ascTime = "%(asctime)s ";
    levelName = "%(levelname)s ";
    #pathName = "%(pathname)s \n";
    module = "%(module)s ";
    functionName = "%(funcName)s ";
    lineNumber = "%(lineno)d \n";
    message = "%(message)s \n";

    logFormat = init + ascTime + levelName + module + functionName + lineNumber + message
    return logFormat

