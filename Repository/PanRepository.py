from Entity import _RawText as RawText
from Entity import _Detection as Detection
from Entity import _RawTextExcerptLocation as RawTextExcerptLocation
from Entity import _DetectionPanXmlPlain as DetectionPanXmlPlain
from Constant import _PanDetectionXmlStructure as PanDetectionXmlStructure
import os
from xml.dom import minidom

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

    def GetTupleFileNameSuspiciousSourceList(self, pairsFilePath):
        tupleFileNameList = []
        with open(pairsFilePath, 'r') as pairsFile:
            for pairsFileLine in pairsFile:
                suspiciousFileName, sourceFileName = pairsFileLine.split()
                tupleFileNameList.append((suspiciousFileName, sourceFileName))
        return tupleFileNameList

    def GetDetectionPanXmlPlainListFromFile(self, filePath):
        documentStructure = PanDetectionXmlStructure.Structure
        featureStruture = documentStructure.featureChild
        documentXml = minidom.parse(filePath).getElementsByTagName(
            name = documentStructure.DOCUMENT)[0]
        _suspiciousFileName = documentXml.attributes[documentStructure.attributes.REFERENCE].value
        detectionPanXmlPlainList = []
        for featureXml in documentXml.getElementsByTagName(
            name = featureStruture.FEATURE):
            
            hasName = featureXml.hasAttribute(featureStruture.attributes.NAME)
            hasObfuscation = featureXml.hasAttribute(featureStruture.attributes.OBFUSCATION)
            hasObfuscationDegree = featureXml.hasAttribute(featureStruture.attributes.OBFUSCATION_DEGREE)
            hasType = featureXml.hasAttribute(featureStruture.attributes.TYPE)
            hasSuspiciousLength = featureXml.hasAttribute(featureStruture.attributes.THIS_LENGTH)
            hasSuspiciousOffset = featureXml.hasAttribute(featureStruture.attributes.THIS_OFFSET)
            hasSourceLength = featureXml.hasAttribute(featureStruture.attributes.SOURCE_LENGTH)
            hasSourceOffset = featureXml.hasAttribute(featureStruture.attributes.SOURCE_OFFSET)
            hasSourceFileName = featureXml.hasAttribute(featureStruture.attributes.SOURCE_REFERENCE)
            
            detectionPanXmlPlain = DetectionPanXmlPlain(
                name = featureXml.attributes[featureStruture.attributes.NAME].value if hasName else None,
                obfuscation = featureXml.attributes[featureStruture.attributes.OBFUSCATION].value if hasObfuscation else None,
                obfuscationDegree = featureXml.attributes[featureStruture.attributes.OBFUSCATION_DEGREE].value if hasObfuscationDegree else None,
                _type = featureXml.attributes[featureStruture.attributes.TYPE].value if hasType else None,
                suspiciousLength = featureXml.attributes[featureStruture.attributes.THIS_LENGTH].value if hasSuspiciousLength else None,
                suspiciousOffset = featureXml.attributes[featureStruture.attributes.THIS_OFFSET].value if hasSuspiciousOffset else None,
                sourceLength = featureXml.attributes[featureStruture.attributes.SOURCE_LENGTH].value if hasSourceLength else None,
                sourceOffset = featureXml.attributes[featureStruture.attributes.SOURCE_OFFSET].value if hasSourceOffset else None,
                sourceFileName = featureXml.attributes[featureStruture.attributes.SOURCE_REFERENCE].value if hasSourceFileName else None,
                suspiciousFileName = _suspiciousFileName)
            detectionPanXmlPlainList.append(detectionPanXmlPlain)
        return detectionPanXmlPlainList

    def GetDetectionPanXmlPlainListFromDiretory(self, filesFolderPath):
        xmlFilesNames = []
        for _file in os.listdir(filesFolderPath):
            if _file.endswith(".xml"):
                xmlFilesNames.append(_file)
        detectionPanXmlPlainList = []
        for xmlFileName in xmlFilesNames:
            xmlFilePath = os.path.join(filesFolderPath, xmlFileName)
            detectionPanXmlPlainListFromFile = self.GetDetectionPanXmlPlainListFromFile(
                filePath = xmlFilePath)
            detectionPanXmlPlainList = detectionPanXmlPlainList + detectionPanXmlPlainListFromFile
        return detectionPanXmlPlainList

    def Hello(self):
        print ('Hello, I\'m a repository')
