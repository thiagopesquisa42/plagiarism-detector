#!/usr/bin/env python

import os
import string
import sys
import xml.dom.minidom
import codecs
import re
from pandas import read_csv
from numpy import array, transpose

plagiarismClassHeader = 'plagiarismClass'
plagiarismClassNameHeader = 'plagiarismClassName'
excerptSourceOffsetFromBeginHeader = 'excerptSourceOffsetFromBegin'
excerptSourceLengthHeader = 'excerptSourceLength'
excerptSourceTextHeader = 'excerptSourceText'
excerptSourceLocationOfFileHeader = 'excerptSourceLocationOfFile'
excerptSuspiciousOffsetFromBeginHeader = 'excerptSuspiciousOffsetFromBegin'
excerptSuspiciousLengthHeader = 'excerptSuspiciousLength'
excerptSuspiciousTextHeader = 'excerptSuspiciousText'
excerptSuspiciousLocationOfFileHeader = 'excerptSuspiciousLocationOfFile'

class PlagiarismClass():
    NO_PLAGIARISM_CLASS = 0
    DIRECT_PLAGIARISM_CLASS = 1
    OBFUSCATED_PLAGIARISM_CLASS = 2

    def getPlagiarismClassNameByClassId(classId):
        switcher = {
            NO_PLAGIARISM_CLASS: "NoPlagiarism",
            DIRECT_PLAGIARISM_CLASS: "DirectPlagiarism",
            OBFUSCATED_PLAGIARISM_CLASS: "ObfuscatedPlagiarism"
        }
        return switcher.get(classId, "Unknown")

class EvidenceLinearRegister():
    tag = 'detected-plagiarism'
    _type = 'artificial'
    plagiarismClass = None
    plagiarismClassName = None
    excerptSourceOffsetFromBegin = None
    excerptSourceLength = None
    excerptSourceText = None
    excerptSourceLocationOfFile = None
    excerptSuspiciousOffsetFromBegin = None
    excerptSuspiciousLength = None
    excerptSuspiciousText = None
    excerptSuspiciousLocationOfFile = None

    def __init__(self, _plagiarismClass, _plagiarismClassName,
        _excerptSourceOffsetFromBegin, _excerptSourceLength, _excerptSourceText,
        _excerptSourceLocationOfFile, _excerptSuspiciousOffsetFromBegin, _excerptSuspiciousLength, 
        _excerptSuspiciousText, _excerptSuspiciousLocationOfFile):
        self.plagiarismClass = _plagiarismClass
        self.plagiarismClassName = _plagiarismClassName
        self.excerptSourceOffsetFromBegin = _excerptSourceOffsetFromBegin
        self.excerptSourceLength = _excerptSourceLength
        self.excerptSourceText = _excerptSourceText
        self.excerptSourceLocationOfFile = _excerptSourceLocationOfFile
        self.excerptSuspiciousOffsetFromBegin = _excerptSuspiciousOffsetFromBegin
        self.excerptSuspiciousLength = _excerptSuspiciousLength
        self.excerptSuspiciousText = _excerptSuspiciousText
        self.excerptSuspiciousLocationOfFile = _excerptSuspiciousLocationOfFile

class Feature():
    name = None
    obfuscation = None
    # obfuscationDegree = None
    sourceLength = None
    sourceOffset = None
    sourceReference = None
    thisLength = None
    thisOffset = None
    _type = None

    def ConvertEvidenceLinearRegisterIntoFeature(self, evidenceLinearRegister):
        self.name = evidenceLinearRegister.tag
        self._type = evidenceLinearRegister._type
        self.obfuscation = evidenceLinearRegister.plagiarismClassName
        self.sourceLength = evidenceLinearRegister.excerptSourceLength
        self.sourceOffset = evidenceLinearRegister.excerptSourceOffsetFromBegin
        self.sourceReference = evidenceLinearRegister.excerptSourceLocationOfFile
        self.thisLength = evidenceLinearRegister.excerptSuspiciousLength
        self.thisOffset = evidenceLinearRegister.excerptSuspiciousOffsetFromBegin

class Detection():
    suspiciousDocumentFileName = None
    sourceDocumentFileName = None
    features = []

    def __init__(self, _suspiciousDocumentFileName, _sourceDocumentFileName):
        self.suspiciousDocumentFileName = _suspiciousDocumentFileName
        self.sourceDocumentFileName = _sourceDocumentFileName

    def ConvertDetectionIntoXmlAndSave(self):
        impl = xml.dom.minidom.getDOMImplementation()
        doc = impl.createDocument(None, 'document', None)
        root = doc.documentElement
        root.setAttribute('reference', self.suspiciousDocumentFileName)
        doc.createElement('feature')

        for _feature in self.features:
            feature = doc.createElement('feature')
            feature.setAttribute('name', _feature.name)
            feature.setAttribute('this_offset', str(_feature.thisOffset))
            feature.setAttribute('this_length', str(_feature.thisLength))
            feature.setAttribute('source_reference', _feature.sourceReference)
            feature.setAttribute('source_offset', str(_feature.sourceOffset))
            feature.setAttribute('source_length', str(_feature.sourceLength))
            root.appendChild(feature)

        outDirectory = 'C:/plagiarism_detector_files_base/'+'detections/poc/'
        doc.writexml(
            open(
                outDirectory + 
                self.suspiciousDocumentFileName.split('.')[0] + '-' + 
                self.sourceDocumentFileName.split('.')[0] + '.xml',
                'w'),
            encoding='utf-8')

def ConvertEvidenceLinearRegisterListIntoFeatureList(evidenceList):
    features = []
    for evidence in evidenceList:
        feature = Feature()
        feature.ConvertEvidenceLinearRegisterIntoFeature(evidence)
        features.append(feature)
    return features

# Carregando dados
database = read_csv(
    'C:/plagiarism_detector_files_base/'+'linearRegisters/annotations_features.csv',
    sep = ";", encoding = "ISO-8859-1")

groupedEvidenceList = database.groupby([excerptSuspiciousLocationOfFileHeader, excerptSourceLocationOfFileHeader])
groupsKeys = list(groupedEvidenceList.groups.keys())

detectionList = [
    Detection(
        _suspiciousDocumentFileName = suspiciousDocumentFileName, 
        _sourceDocumentFileName = sourceDocumentFileName
    )
    for suspiciousDocumentFileName, sourceDocumentFileName in groupsKeys
]

for detection in detectionList:
    dataBaseSelectBySuspiciousAndSourceFile = groupedEvidenceList.get_group((
        detection.suspiciousDocumentFileName,
        detection.sourceDocumentFileName
    ))
    dataBaseIndexes = list(dataBaseSelectBySuspiciousAndSourceFile.index)
    evidenceList = [
        EvidenceLinearRegister(
            _plagiarismClass = dataBaseSelectBySuspiciousAndSourceFile[plagiarismClassHeader][index],
            _plagiarismClassName = dataBaseSelectBySuspiciousAndSourceFile[plagiarismClassNameHeader][index],
            _excerptSourceOffsetFromBegin = dataBaseSelectBySuspiciousAndSourceFile[excerptSourceOffsetFromBeginHeader][index],
            _excerptSourceLength = dataBaseSelectBySuspiciousAndSourceFile[excerptSourceLengthHeader][index],
            _excerptSourceText = dataBaseSelectBySuspiciousAndSourceFile[excerptSourceTextHeader][index],
            _excerptSourceLocationOfFile = dataBaseSelectBySuspiciousAndSourceFile[excerptSourceLocationOfFileHeader][index],
            _excerptSuspiciousOffsetFromBegin = dataBaseSelectBySuspiciousAndSourceFile[excerptSuspiciousOffsetFromBeginHeader][index],
            _excerptSuspiciousLength = dataBaseSelectBySuspiciousAndSourceFile[excerptSuspiciousLengthHeader][index],
            _excerptSuspiciousText = dataBaseSelectBySuspiciousAndSourceFile[excerptSuspiciousTextHeader][index],
            _excerptSuspiciousLocationOfFile = dataBaseSelectBySuspiciousAndSourceFile[excerptSuspiciousLocationOfFileHeader][index]
        )
        for index in dataBaseIndexes]
    features = ConvertEvidenceLinearRegisterListIntoFeatureList(evidenceList)
    detection.features = features

for detection in detectionList:
    detection.ConvertDetectionIntoXmlAndSave()
















