import logging

class BaseProcess(object):
    def setLogger(self):
        init = "\n"
        ascTime = "%(asctime)s ";
        levelName = "%(levelname)s ";
        pathName = "%(pathname)s \n";
        module = "%(module)s ";
        functionName = "%(funcName)s ";
        lineNumber = "%(lineno)d \n";
        message = "%(message)s \n";

        logFormat = init + ascTime + levelName + pathName + module + functionName + lineNumber + message
        logger = logging.getLogger(name = 'process')
        fileHandler = logging.FileHandler('logging.process.log')
        formatter = logging.Formatter(logFormat)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler) 
        logger.setLevel(logging.INFO)
                
        infoLogStruct = "\n ascTime levelName pathName \n module funcName lineNumber \n message \n"
        logger.info("This log has the struct: " + infoLogStruct)
        self.logger = logger

    logger = None

    def __init__(self):
        self.setLogger()