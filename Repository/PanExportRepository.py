from Repository import _BaseRepository as BaseRepository
from Entity import _PanDetectionXmlStructure as PanDetectionXmlStructure
from constant import Contexts, PanSettings
from xml.dom import minidom
import os

class PanExportRepository(BaseRepository):

    def StoreMultipleXml(self, detectionGroupOfListFromRawTextPair, folderNickname):
        try:
            uniqueFolderPath = self.GetUniqueFolderPath(folderNickname)
            bytesLength = 0
            for detectionListFromRawTextPair in detectionGroupOfListFromRawTextPair:
                xmlFileContent = PanExportRepository.CastDetectionListToPanFormat(
                    detectionListFromRawTextPair)
                fileWriter = self.GetXmlFileWriter(detectionListFromRawTextPair.rawTextPair, uniqueFolderPath)
                fileWriter.write(xmlFileContent)
                fileWriter.close()
                bytesLength += os.path.getsize(fileWriter.name)
        except Exception as exception:
            self.logger.exception('failure when storing item, error ' + str(exception))
            raise exception
        else:
            storedLength = BaseRepository.HumanizeBytes(bytes = bytesLength)
            self.logger.info('item stored: ' + '.xml files' +\
            ' ' + storedLength  + ' at folder ' + uniqueFolderPath)

    def StoreXml(self, detectionListFromRawTextPair):
        try:
            xmlFileContent = PanExportRepository.CastDetectionListToPanFormat(
                detectionListFromRawTextPair)
            fileWriter = self.GetXmlFileWriter(detectionListFromRawTextPair.rawTextPair, self.GetPath())
            fileWriter.write(xmlFileContent)
        except Exception as exception:
            self.logger.exception('failure when storing item, error ' + str(exception))
            raise exception
        else:
            fileWriter.close()
            storedLength = BaseRepository.HumanizeBytes(bytes = os.path.getsize(fileWriter.name))
            self.logger.info('item stored: ' + str(type(xmlFileContent)) +\
            ' ' + storedLength + ' ' + fileWriter.name)
            return fileWriter.name
    
    def CastDetectionListToPanFormat(detectionListFromRawTextPair):
        detectionList = detectionListFromRawTextPair.detectionList
        documentStructure = PanDetectionXmlStructure.Document
        suspiciousFileName = detectionListFromRawTextPair.rawTextPair.suspiciousRawText.fileName
        
        document = minidom.getDOMImplementation().createDocument(None, documentStructure.DOCUMENT, None)
        documentRoot = document.documentElement
        documentRoot.setAttribute(documentStructure.Attributes.REFERENCE, suspiciousFileName)
        for detection in detectionList:
            thisOffset = str(detection.rawTextSuspiciousLocation.firstCharacterPosition)
            thisLength = str(detection.rawTextSuspiciousLocation.stringLength)
            sourceReference = detection.rawTextPair.sourceRawText.fileName
            sourceOffset = str(detection.rawTextSourceLocation.firstCharacterPosition)
            sourceLength = str(detection.rawTextSourceLocation.stringLength)

            feature = document.createElement(documentStructure.Feature.FEATURE)
            feature.setAttribute(documentStructure.Feature.Attributes.NAME, PanSettings.detectionName)
            feature.setAttribute(documentStructure.Feature.Attributes.THIS_OFFSET, thisOffset)
            feature.setAttribute(documentStructure.Feature.Attributes.THIS_LENGTH, thisLength)
            feature.setAttribute(documentStructure.Feature.Attributes.SOURCE_REFERENCE, sourceReference)
            feature.setAttribute(documentStructure.Feature.Attributes.SOURCE_OFFSET, sourceOffset)
            feature.setAttribute(documentStructure.Feature.Attributes.SOURCE_LENGTH, sourceLength)
            documentRoot.appendChild(feature)
        return document.toprettyxml()
    
    def GetXmlFileWriter(self, rawTextPair, folderPath):
        xmlFileName = self.GetXmlFileName(rawTextPair)
        xmlFilePath = os.path.join(folderPath, xmlFileName)
        return open(xmlFilePath, 'w')

    def GetXmlFileName(self, rawTextPair):
        suspiciousName = rawTextPair.suspiciousRawText.fileName.split('.')[0]
        sourceName = rawTextPair.sourceRawText.fileName.split('.')[0]
        return suspiciousName + '-' + sourceName + '.xml'

    def __init__(self):
        super().__init__(context = Contexts.PAN_FORMAT_DETECTIONS, name = 'PanExport')
