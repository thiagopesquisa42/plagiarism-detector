import os

class LoggerConstant():
    class Name():
        REPOSITORY = 'repository'
        INTERNAL = 'internal'
        PROCESS = 'process'
        MANAGER = 'manager'
        VIEW = 'view'

    class File():
        MAXIMUM_SIZE_MEGABYTES = 10
        FOLDER_PATH = 'log'
        BIG_LOG_FOLDER_PATH = os.path.join(FOLDER_PATH, 'big')
        FILE_EXTENSION = '.log'
        REPOSITORY = os.path.join(FOLDER_PATH, 'repository' + FILE_EXTENSION)
        INTERNAL = os.path.join(FOLDER_PATH, 'internal' + FILE_EXTENSION)
        PROCESS = os.path.join(FOLDER_PATH, 'process' + FILE_EXTENSION)
        MANAGER = os.path.join(FOLDER_PATH, 'manager' + FILE_EXTENSION)
        VIEW = os.path.join(FOLDER_PATH, 'view' + FILE_EXTENSION)


