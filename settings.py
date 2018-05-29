import os

global rootLocation
global currentSubFolder
currentSubFolder = 'none'
rootLocation = 'data'
subFolderDefault = 'newFolder'
TRAINING_SUBFOLDER = 'train'
TESTING_SUBFOLDER = 'test'

def SetRootLocation(rootLocationName):
    global rootLocation
    rootLocation = os.path.join('data', rootLocationName)

def SetCurrentSubFolder(subFolderName):
    global currentSubFolder
    currentSubFolder = subFolderName