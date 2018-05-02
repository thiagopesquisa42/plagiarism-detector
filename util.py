from constant import LoggerConstant
import os
from datetime import datetime

class LoggerUtil():
    @staticmethod
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

    @staticmethod
    def HandleAllLogsFilesSize():
        logFilePathList = []
        for fileName in os.listdir(LoggerConstant.File.FOLDER_PATH):
            if fileName.endswith(LoggerConstant.File.FILE_EXTENSION):
                logFilePathList.append(os.path.join(LoggerConstant.File.FOLDER_PATH, fileName))
        for logFilePath in logFilePathList:
            LoggerUtil.HandleLogFileSize(logFilePath)

    @staticmethod
    def HandleLogFileSize(logFilePath):
        if(not os.path.isfile(logFilePath)):
            return
        logMaximumBytes = LoggerConstant.File.MAXIMUM_SIZE_MEGABYTES << 20
        if(LoggerUtil.GetCurrentLogLength(logFilePath) < logMaximumBytes):
            return
        else:
            LoggerUtil.MoveLogFile(logFilePath)
    
    @staticmethod
    def GetCurrentLogLength(filePath):
        sizeOfLog = os.path.getsize(filename = filePath)
        return sizeOfLog
    
    @staticmethod
    def MoveLogFile(logFilePath):
        fileFolder, fileName = os.path.split(logFilePath)
        dateTimeString = datetime.now().strftime('%Y%m%d_%H%M%S')
        fileNewName = fileName.split(LoggerConstant.File.FILE_EXTENSION)[0] + '.' + dateTimeString + LoggerConstant.File.FILE_EXTENSION
        os.rename(src = logFilePath, dst = os.path.join(LoggerConstant.File.BIG_LOG_FOLDER_PATH, fileNewName))

if(not os.path.exists(LoggerConstant.File.FOLDER_PATH)):
    os.makedirs(LoggerConstant.File.FOLDER_PATH)
if(not os.path.exists(LoggerConstant.File.BIG_LOG_FOLDER_PATH)):
    os.makedirs(LoggerConstant.File.BIG_LOG_FOLDER_PATH)
LoggerUtil.HandleAllLogsFilesSize()