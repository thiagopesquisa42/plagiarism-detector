from Util import _LoggerUtil as LoggerUtil
from Util import _ContextManager as ContextManager
from constant import PanDataBaseLocation, Contexts, ClassifiersNickNames
from Process import _DataImportationProcess as DataImportationProcess
from Process import _PreProcessingRawTextProcess as PreProcessingRawTextProcess
from Process import _SeedingProcess as SeedingProcess
from Process import _SeedingDataProcess as SeedingDataProcess
from Process import _SeedingClassifierProcess as SeedingClassifierProcess
from Process import _PanExportProcess as PanExportProcess
from Process import _PanEvaluateProcess as PanEvaluateProcess
import os

def ProcessTrainData():
    # ImportTrainDataBase()
    CommomProcessing(context = Contexts.TRAIN)

def ProcessTestData():
    # ImportTestDataBase()
    CommomProcessing(context = Contexts.TEST)

def ImportTrainDataBase():
    _dataImportationProcess = DataImportationProcess(context = Contexts.TRAIN)
    trainTextCollectionMeta = _dataImportationProcess.ImportTrainDataBaseFromPanFiles(
        # folderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TRAIN_JANUARY_020_P, 
        # description = 'treino, base pan 2013-jan 020%',
        # folderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TRAIN_JANUARY_001_P, 
        # description = 'treino, base pan 2013-jan 001%',
        folderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TRAIN_JANUARY_005_P, 
        description = 'treino, base pan 2013-jan 005%',
        originalCreationDate = '2013-01-21')

def ImportTestDataBase():
    _dataImportationProcess = DataImportationProcess(context = Contexts.TEST)
    testTextCollectionMeta = _dataImportationProcess.ImportTrainDataBaseFromPanFiles(
        # folderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TEST2_JANUARY_020_P, 
        # description = 'teste, base pan 2013-jan 020%',
        # folderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TEST2_JANUARY_001_P, 
        # description = 'teste, base pan 2013-jan 001%',
        folderCompletePath = PanDataBaseLocation.subSampled.FOLDER_PATH_2013_TEST2_JANUARY_005_P, 
        description = 'teste, base pan 2013-jan 005%',
        originalCreationDate = '2013-01-21')

def CommomProcessing(context):
    _preProcessingRawTextProcess = PreProcessingRawTextProcess(context = context)
    preProcessedData = _preProcessingRawTextProcess.PreProcessing()
    _seedingProcess = SeedingProcess(context = context)
    preProcessedData = _seedingProcess.SeedingProcessing()
    _seedingDataProcess = SeedingDataProcess(context = context)
    dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingData()

def CreateSummaryDrivenDataFrame():
    _seedingDataProcess = SeedingDataProcess(context = Contexts.TRAIN)
    dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingDataSummaryDriven()
    _seedingDataProcess = SeedingDataProcess(context = Contexts.TEST)
    dataFrame = _seedingDataProcess.CreateSeedingDataFrameFromSeedingDataSummaryDriven()

def TrainingClassifier(classifierNickName):
    _seedingClassifierProcess = SeedingClassifierProcess()
    classifierMetaTrained = _seedingClassifierProcess.TrainSeedClassifier(classifierNickName)

def TestingClassifier():
    _seedingClassifierProcess = SeedingClassifierProcess()
    reportList = _seedingClassifierProcess.TestSeedClassifier()
    return reportList

def ExportDetectionToPan():
    _panExportProcess = PanExportProcess()
    return _panExportProcess.ExportPanFormattedDetections()

def GenerateIdealClassifier():
    _seedingDataProcess = SeedingDataProcess(context = Contexts.TEST)
    _seedingDataProcess.ExportIdealClassifier()
    _seedingClassifierProcess = SeedingClassifierProcess()
    classifierMetaTested = _seedingClassifierProcess.ExportExperimentResults()

def PanEvaluation(folderPath_Class_TupleList):
    _panEvaluateProcess = PanEvaluateProcess()
    panReportList = _panEvaluateProcess.EvaluateAndStore(folderPath_Class_TupleList)
    return panReportList

def ConvertReportsToFlatRow(reportList, panReportList, getHeaderOnly = False):
    rowReport = []
    for report in reportList:
        rowReport.extend(
            [value if (not getHeaderOnly) else key 
                for key, value in report.items()]
        )
        rowReport.append(' _ ')
    for panReport in panReportList:
        rowReport.extend(
            [value if (not getHeaderOnly) else key
                for key, value in panReport['metrics'].items()]
        )
        rowReport.append(' _ ')
    return rowReport

def SaveReportFlatMatrix(reportFlatMatrix, classifierNickName):
    import pandas
    from datetime import datetime
    dataFrameReport = pandas.DataFrame(reportFlatMatrix[1:], columns=reportFlatMatrix[0])
    dateTimeString = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    fileName = 'data\\reportFull-' + classifierNickName + '-' + dateTimeString + '.csv'
    dataFrameReport.to_csv(fileName, sep=',', encoding='utf-8')

def Main():
    # experimentName = 'experiment005p_tape001'
    # experimentName = 'experiment005p_tape002'
    # experimentName = 'experiment020p_tape003_binario_randomSample'
    # experimentName = 'experiment001p_tape004'
    # experimentName = 'experiment005p_tape005_randomSample'
    # experimentName = 'experiment005p_tape006_iblrn_trainOnly'
    # experimentName = 'experiment005p_tape007_noiblrnMyApproache_trainOnly'
    # experimentName = 'experiment005p_tape008_noiblrnMyApproache_trainOnly'
    # experimentName = 'experiment005p_tape009_idealClassifier'
    # experimentName = 'experiment005p_tape010_iblrn'
    # experimentName = 'experiment005p_tape011_multiClass_randomSample'
    # experimentName = 'experiment005p_tape012_contagem_base_dados'
    # experimentName = 'experiment005p_tape005_randomSample_for30times'
    # experimentName = 'experiment005p_tape011_multiClass_randomSample_for30times'
    experimentName = 'experiment020p_tape003_binario_randomSample_for30times'
    # ContextManager.InitExperiment(experimentUniqueName = experimentName)
    ContextManager.ContinueExperiment(experimentUniqueName = experimentName)
    # ProcessTrainData()
    # ProcessTestData()
    # CreateSummaryDrivenDataFrame()
    classifierList = [
        ClassifiersNickNames.DECISION_TREE,
        ClassifiersNickNames.RANDOM_FOREST,
        ClassifiersNickNames.ADABOOST_DECISION_TREE]
    
    for classifierNickName in classifierList:
        print(classifierNickName.name, 'started')
        reportFlatMatrix = []
        headerOk = False
        times = 30
        for i in range(times):    
            print(i, 'started')
            TrainingClassifier(classifierNickName)
            reportList = TestingClassifier()
            folderPath_Class_TupleList = ExportDetectionToPan()
            panReportList = PanEvaluation(folderPath_Class_TupleList)
            reportFlatRow = ConvertReportsToFlatRow(reportList, panReportList)
            reportFlatMatrix.append(reportFlatRow)
            if(not headerOk):
                reportFlatRowHeader = ConvertReportsToFlatRow(reportList, panReportList, getHeaderOnly = True)
                reportFlatMatrix.insert(0, reportFlatRowHeader)
                headerOk = True
            print(i, 'finished')            
        SaveReportFlatMatrix(reportFlatMatrix, classifierNickName.name)

    # _seedingClassifierProcess = SeedingClassifierProcess()
    # _seedingClassifierProcess.ExportClassifierGraphviz()
    # GenerateIdealClassifier()
    # ExportDetectionToPan()

Main()