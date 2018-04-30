from Entity import _RawText as RawText
import os

class PanRepository():

    def GetTextFromFile(self, filePath):
        with open(filePath, 'r', encoding="utf-8") as _file:
            text = _file.read().encode(encoding='UTF-8',errors='namereplace')
            return text
    
    def GetRawTextListFromDirectoryOfTexts(self, filesFolderPath, rawTextType, textCollectionMetaId):
        textFilesNames = []
        for _file in os.listdir(filesFolderPath):
            if _file.endswith(".txt"):
                textFilesNames.append(_file)
        rawTextList = []
        for textFileName in textFilesNames:
            textFilePath = os.path.join(filesFolderPath, textFileName)
            text = self.GetTextFromFile(filePath = textFilePath)
            rawText = RawText(
                _type = rawTextType,
                textCollectionMetaId = textCollectionMetaId, 
                fileName = textFileName, 
                text = text)
            rawTextList.append(rawText)
        return rawTextList

    def Hello(self):
        print ('Hello, I\'m a repository')
