from Entity import _RawText as RawText
from Entity import _Detection as Detection
from Entity.PreProcessing import _RawTextExcerptLocation as RawTextExcerptLocation
from Entity import _PanDetectionXmlPlain as PanDetectionXmlPlain
from Entity import _PanDetectionXmlStructure as PanDetectionXmlStructure
import os
from xml.dom import minidom

class PanRepository():

    def GetTextFromFile(self, filePath):
        with open(filePath, 'r', encoding="utf-8") as _file:
            text = _file.read().encode(encoding='UTF-8',errors='namereplace')
            return text
    
    def GetRawTextListFromDirectoryOfTexts(self, filesFolderPath, rawTextType, textCollectionMeta):
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
                textCollectionMeta = textCollectionMeta, 
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
    
    def UpdatePairsFile(self, pairsFilePath, pairsLines):
        try:
            with open(pairsFilePath, 'w') as pairsFile:
                pairsFile.write('\n'.join(pairsLines))
        except Exception as exception:
            raise exception

    def GetPanDetectionXmlPlainListFromFile(self, filePath):
        documentStructure = PanDetectionXmlStructure.Document
        featureStruture = documentStructure.Feature
        documentXml = minidom.parse(filePath).getElementsByTagName(
            name = documentStructure.DOCUMENT)[0]
        _suspiciousFileName = documentXml.attributes[documentStructure.Attributes.REFERENCE].value
        panDetectionXmlPlainList = []
        for featureXml in documentXml.getElementsByTagName(
            name = featureStruture.FEATURE):
            
            hasName = featureXml.hasAttribute(featureStruture.Attributes.NAME)
            hasObfuscation = featureXml.hasAttribute(featureStruture.Attributes.OBFUSCATION)
            hasObfuscationDegree = featureXml.hasAttribute(featureStruture.Attributes.OBFUSCATION_DEGREE)
            hasType = featureXml.hasAttribute(featureStruture.Attributes.TYPE)
            hasSuspiciousLength = featureXml.hasAttribute(featureStruture.Attributes.THIS_LENGTH)
            hasSuspiciousOffset = featureXml.hasAttribute(featureStruture.Attributes.THIS_OFFSET)
            hasSourceLength = featureXml.hasAttribute(featureStruture.Attributes.SOURCE_LENGTH)
            hasSourceOffset = featureXml.hasAttribute(featureStruture.Attributes.SOURCE_OFFSET)
            hasSourceFileName = featureXml.hasAttribute(featureStruture.Attributes.SOURCE_REFERENCE)
            
            if(hasType and hasSuspiciousLength and
                hasSuspiciousOffset and hasSourceLength and hasSourceOffset and
                hasSourceFileName):
                panDetectionXmlPlain = PanDetectionXmlPlain(
                    name = featureXml.attributes[featureStruture.Attributes.NAME].value if hasName else None,
                    obfuscation = featureXml.attributes[featureStruture.Attributes.OBFUSCATION].value if hasObfuscation else None,
                    obfuscationDegree = float(featureXml.attributes[featureStruture.Attributes.OBFUSCATION_DEGREE].value) if hasObfuscationDegree else None,
                    _type = featureXml.attributes[featureStruture.Attributes.TYPE].value if hasType else None,
                    suspiciousLength = int(featureXml.attributes[featureStruture.Attributes.THIS_LENGTH].value) if hasSuspiciousLength else None,
                    suspiciousOffset = int(featureXml.attributes[featureStruture.Attributes.THIS_OFFSET].value) if hasSuspiciousOffset else None,
                    sourceLength = int(featureXml.attributes[featureStruture.Attributes.SOURCE_LENGTH].value) if hasSourceLength else None,
                    sourceOffset = int(featureXml.attributes[featureStruture.Attributes.SOURCE_OFFSET].value) if hasSourceOffset else None,
                    sourceFileName = featureXml.attributes[featureStruture.Attributes.SOURCE_REFERENCE].value if hasSourceFileName else None,
                    suspiciousFileName = _suspiciousFileName)
                if(panDetectionXmlPlain._type in 'translation-chain'):
                    panDetectionXmlPlain.obfuscation = 'translation-chain'
                panDetectionXmlPlainList.append(panDetectionXmlPlain)
            else:
                print('corrupted detection entry found, it was ignored')
        return panDetectionXmlPlainList

    def GetPanDetectionXmlPlainListFromDiretory(self, filesFolderPath):
        xmlFilesNames = []
        for _file in os.listdir(filesFolderPath):
            if _file.endswith(".xml"):
                xmlFilesNames.append(_file)
        panDetectionXmlPlainList = []
        for xmlFileName in xmlFilesNames:
            xmlFilePath = os.path.join(filesFolderPath, xmlFileName)
            panDetectionXmlPlainListFromFile = self.GetPanDetectionXmlPlainListFromFile(
                filePath = xmlFilePath)
            panDetectionXmlPlainList = panDetectionXmlPlainList + panDetectionXmlPlainListFromFile
        return panDetectionXmlPlainList

    def Hello(self):
        print ('Hello, I\'m a repository')
