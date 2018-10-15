from Repository import _BaseRepository as BaseRepository
from constant import Contexts
import os
import json
from datetime import datetime

class PanEvaluateRepository(BaseRepository):

    def StorePanReport(self, panReportList):
        try:
            stringContent = self.CastContentToString(panReportList)
            fileWriter = self.GetReportWriter()
            fileWriter.write(stringContent)
        except Exception as exception:
            self.logger.exception('failure when storing item, error ' + str(exception))
            raise exception
        else:
            fileWriter.close()
            storedLength = BaseRepository.HumanizeBytes(bytes = os.path.getsize(fileWriter.name))
            self.logger.info('item stored: ' + str(type(panReportList)) +\
            ' ' + storedLength + ' ' + fileWriter.name)
            return fileWriter.name

    def GetReportWriter(self):
        fileName = self.GetPanReportFileName()
        filePath = os.path.join(self.GetPath(), fileName)
        return open(filePath, 'w')

    def CastContentToString(self, content):
        stringContent = ''
        if(isinstance(content, dict) or isinstance(content, list)):
            stringContent = self.PrettyDictionary(content)
            stringContent = self.AssureContentEndLines(stringContent)
        else: 
            stringContent = str(content)
        return stringContent

    def PrettyDictionary(self, dictionary, indent = 4):
        return json.dumps(dictionary, indent = indent)

    def AssureContentEndLines(self, stringContent):
        return stringContent.replace('\\n', '\n')

    def GetPanReportFileName(self):
        dateTimeString = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        fileName = self.name + dateTimeString + '.panReport'
        return fileName
    
    def __init__(self):
        super().__init__(context = Contexts.META, name = 'PanResultsExport')
