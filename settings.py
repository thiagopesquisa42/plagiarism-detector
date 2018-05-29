import os

global rootLocation
global currentSubFolder
currentSubFolder = 'none'
rootLocation = 'data'
subFolderDefault = 'newFolder'

def SetRootLocation(rootLocationName):
    global rootLocation
    rootLocation = os.path.join('data', rootLocationName)

def SetCurrentSubFolder(subFolderName):
    global currentSubFolder
    currentSubFolder = subFolderName