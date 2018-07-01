from Repository import _BaseRepository as BaseRepository
from constant import Contexts
import os
import json

class ResultsExportRepository(BaseRepository):

    def StoreReport(self, resultsExport):
        try:
            tupleList_FileName_Content = self.GetTupleList_FileName_Content_FromFileMetaList(
                fileMetaList = resultsExport.fileMetaList)
            folderPath = self.GetUniqueFolderPath(resultsExport.nickname)
            bytesLength = 0
            for fileName, content in tupleList_FileName_Content:
                fileWriter = self.GetReportWriter(folderPath, fileName)
                stringContent = ResultsExportRepository.CastContentToString(content)
                fileWriter.write(stringContent)
                fileWriter.close()
                bytesLength += os.path.getsize(fileWriter.name)
        except Exception as exception:
            self.logger.exception('failure when storing item, error ' + str(exception))
            raise exception
        else:
            storedLength = BaseRepository.HumanizeBytes(bytes = bytesLength)
            self.logger.info('item stored: ' + str(type(resultsExport)) +\
            ' ' + storedLength)

    def GetReportWriter(self, folder, fileName):
        filePath = os.path.join(folder, fileName)
        return open(filePath, 'w')

    def CastContentToString(content):
        stringContent = ''
        if(isinstance(content, dict)):
            stringContent = ResultsExportRepository.PrettyDictionary(content)
            stringContent = ResultsExportRepository.AssureContentEndLines(stringContent)
        else: 
            stringContent = str(content)
        return stringContent

    def PrettyDictionary(dictionary):
        return json.dumps(dictionary, indent = 4)

    def AssureContentEndLines(stringContent):
        return stringContent.replace('\\n', '\n')

    def GetTupleList_FileName_Content_FromFileMetaList(self, fileMetaList):
        tupleList = []
        for fileMeta in fileMetaList:
            if(isinstance(fileMeta.content, list)):
                tupleList.extend(
                    ResultsExportRepository.GetTupleList_FileName_Content_FromContentList(fileMeta))
            else:
                tupleList.append((fileMeta.prefix + fileMeta.suffix, fileMeta.content))
        tupleList.append(('raw.txt', {str(fileMeta.prefix + fileMeta.suffix): fileMeta.content for fileMeta in fileMetaList}))
        return tupleList

    def GetTupleList_FileName_Content_FromContentList(fileMeta):
        fileNameList = ResultsExportRepository.GetFileNameList(
            quantity = len(fileMeta.content), prefix = fileMeta.prefix, suffix = fileMeta.suffix)
        tupleList = []
        for index, content in enumerate(fileMeta.content):
            tupleList.append((fileNameList[index], content))
        return tupleList

    def GetFileNameList(quantity, prefix, suffix):
        stringFormatter = '{0:0' + str(1 + len(str(quantity))) + 'd}'
        return [
            prefix + stringFormatter.format(index) + suffix
            for index in range(1, 1 + quantity)]
    
    def __init__(self):
        super().__init__(context = Contexts.META, name = 'ResultsExport')
