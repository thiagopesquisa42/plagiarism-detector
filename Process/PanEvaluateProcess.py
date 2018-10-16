from Entity import _PlagiarismClass as PlagiarismClass
from Entity import _PanFolderStructure as PanFolderStructure
from Entity import _PlagiarismClass as PlagiarismClass
from Process import _BaseProcess as BaseProcess
from Repository import _PanEvaluateRepository as PanEvaluateRepository
from constant import PanDataBaseLocation, SupportScripts
from pythonOldVersionScriptsProcessCaller import callOldProcess
from distutils.dir_util import copy_tree
from datetime import datetime
import os

class PanEvaluateProcess(BaseProcess):
    def EvaluateAndStore(self, folderPath_Class_TupleList, algorithmNickName):
        try:
            self.logger.info('[PanEvaluateProcess] started')
            panReportList = self.CalculatePanEvaluation(folderPath_Class_TupleList, algorithmNickName)
            reportFileName = self._panEvaluateRepository.StorePanReport(panReportList)
        except Exception as exception:
            self.logger.exception('[PanEvaluateProcess] failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('[PanEvaluateProcess] finished')
            return panReportList
    
    def CalculatePanEvaluation(self, folderPath_Class_TupleList, algorithmNickName):
        currentWorkingDirectory = os.getcwd()
        plagiarismPanDatabasePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TEST2_JANUARY_005_P
        # plagiarismPanDatabasePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TEST2_JANUARY_020_P
        panReportList = []
        for panDetectionFolderPath, _class in folderPath_Class_TupleList:
            pathToScript = os.path.join(currentWorkingDirectory, SupportScripts.FOLDER_PATH_PAN_OFFICIAL_METRIC_SCRIPT) 
            plagiarismPanTargetDatabasePath = plagiarismPanDatabasePath
            if(str(_class) != str(True)):
                plagiarismClassFolderName = PanEvaluateProcess.ConvertPlagiarismClassToDetectionFolderName(_class)
                plagiarismPanTargetDatabasePath = os.path.join(plagiarismPanDatabasePath, plagiarismClassFolderName)
            argumentList = [
                '--plag-path',
                plagiarismPanTargetDatabasePath,
                '--det-path',
                os.path.join(currentWorkingDirectory, panDetectionFolderPath)]
            self.logger.info('old process called: ' + pathToScript + ','.join(argumentList))
            panReportRaw = callOldProcess(
                pathToScript = pathToScript,
                argumentList = argumentList)

            panReport = PanEvaluateProcess.ConvertPanEvaluationOutputToDictionary(panReportRaw, _class)
            panReportList.append(panReport)
        if(len(folderPath_Class_TupleList) > 1):
            panReport = self.CalculatePanEvaluationTotal(folderPath_Class_TupleList, newFolderNickName = algorithmNickName)
            panReportList.append(panReport)
        return panReportList

    def CalculatePanEvaluationTotal(self, folderPath_Class_TupleList, newFolderNickName):
        tempFolderRootPath = self.CopyPanExportedFilesToTempFolder(folderPath_Class_TupleList, newFolderNickName)
        currentWorkingDirectory = os.getcwd()
        plagiarismPanDatabasePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TEST2_JANUARY_005_P
        # plagiarismPanDatabasePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TEST2_JANUARY_020_P
        panReportList = []
        pathToScript = os.path.join(currentWorkingDirectory, SupportScripts.FOLDER_PATH_PAN_OFFICIAL_METRIC_SCRIPT) 
        argumentList = [
            '--plag-path',
            plagiarismPanDatabasePath,
            '--det-path',
            os.path.join(currentWorkingDirectory, tempFolderRootPath)]
        self.logger.info('old process called: ' + pathToScript + ','.join(argumentList))
        panReportRaw = callOldProcess(
            pathToScript = pathToScript,
            argumentList = argumentList)
        panReport = PanEvaluateProcess.ConvertPanEvaluationOutputToDictionary(panReportRaw, 'plagiarism')
        return panReport

    def CopyPanExportedFilesToTempFolder(self, folderPath_Class_TupleList, newFolderNickName):
        if(newFolderNickName is None):
            newFolderNickName = ""
        dateTimeString = datetime.now().strftime('%Y%m%d_%H%M%S')
        tempFolderRootPath =\
            os.path.join('data','temp',
                newFolderNickName + dateTimeString)
        if(not os.path.exists(tempFolderRootPath)):
            os.makedirs(tempFolderRootPath)
        for panDetectionFolderPath, _class in folderPath_Class_TupleList:
            panDetectionFolder = os.path.basename(os.path.normpath(panDetectionFolderPath))
            tempFolderCompletePath = os.path.join(tempFolderRootPath, panDetectionFolder)
            if(not os.path.exists(tempFolderCompletePath)):
                os.makedirs(tempFolderCompletePath)
            self.CopyEntireFolder(panDetectionFolderPath, tempFolderCompletePath)
        return tempFolderRootPath

    def CopyEntireFolder(self, folder, newFolderPath):
        # External source code from here: https://stackoverflow.com/questions/15034151/copy-directory-contents-into-a-directory-with-python
        copy_tree(src = folder, dst = newFolderPath, 
            preserve_mode = True, preserve_times = True, preserve_symlinks = True)

    def ConvertPlagiarismClassToDetectionFolderName(plagiarismClass):
        if(plagiarismClass in [PlagiarismClass.direct, PlagiarismClass.direct.name]):
            return PanFolderStructure.NO_OBFUSCATION_DETECTION_FOLDER
        if(plagiarismClass in [PlagiarismClass.obfuscatedRandom, PlagiarismClass.obfuscatedRandom.name]):
            return PanFolderStructure.RANDOM_OBFUSCATION_DETECTION_FOLDER
        if(plagiarismClass in [PlagiarismClass.obfuscatedSummary, PlagiarismClass.obfuscatedSummary.name]):
            return PanFolderStructure.SUMMARY_OBFUSCATION_DETECTION_FOLDER
        if(plagiarismClass in [PlagiarismClass.obfuscatedTranslation, PlagiarismClass.obfuscatedTranslation.name]):
            return PanFolderStructure.TRANSLATION_OBFUSCATION_DETECTION_FOLDER
        raise TypeError("unknown plagiarism-class, convertion to folder-name failed")

    def ConvertPanEvaluationOutputToDictionary(panReportRaw, _class):
        dictionary = {
            'plagiarismPath': panReportRaw[0],
            'detectionPath' : panReportRaw[1],
            'metrics'       :{
                'plagdet'           : panReportRaw[3].split(' ')[-1],
                'recall'            : panReportRaw[4].split(' ')[-1],
                'precision'         : panReportRaw[5].split(' ')[-1],
                'granularity'       : panReportRaw[6].split(' ')[-1],
                'casesQuantity'     : panReportRaw[7].split(' ')[-1],
                'detectionsQuantity': panReportRaw[8].split(' ')[-1],
                'class'             : str(_class)
            },
            'owner'         : 'pan official metrics script',
        }
        return dictionary

    def __init__(self):
        self._panEvaluateRepository = PanEvaluateRepository()
        super().__init__()
