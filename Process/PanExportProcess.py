from Entity import _Detection as Detection
from Entity import _PlagiarismClass as PlagiarismClass
from Entity import _Detection as Detection
from Entity import _DetectionListFromRawTextPair as DetectionListFromRawTextPair
from Entity import _EnumYesNo as EnumYesNo
from Process import _BaseProcess as BaseProcess
from Repository.Classifier import _ClassifierMetaRepository as ClassifierMetaRepository
from Repository import _PanExportRepository as PanExportRepository
from constant import SeedAttributesNames, PanSettings

class PanExportProcess(BaseProcess):
    def ExportPanFormattedDetections(self):
        try:
            self.logger.info('[Export Pan Formatted Detections] started')

            self.logger.info('getting meta-data-frame')
            classifierMeta = self._classifierMetaRepository.Get()
            metaDataFrame = classifierMeta.metaDataFrame

            self.logger.info('removing not detections')
            metaDataFrame = self.RemoveNotDetections(metaDataFrame)      

            self.logger.info('grouping by raw-text-pair')
            groupedByRawTextPairMetaDataFrame = self.GroupByRawTextPair(metaDataFrame)
            
            self.logger.info('cast to detection groups')
            detectionGroups = self.CastToDetectionGroupsByRawTextPair(groupedByRawTextPairMetaDataFrame)

            self.logger.info('exporting groups')
            self._panExportRepository.StoreMultipleXml(detectionGroups)

        except Exception as exception:
            self.logger.exception('[Export Pan Formatted Detections] failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('[Export Pan Formatted Detections] finished')
    
    def RemoveNotDetections(self, metaDataFrame):
        classes = len(metaDataFrame.plagiarismClass.unique())
        if(classes == 2):
            metaDataFrame = metaDataFrame[(metaDataFrame.classifierPrediction == True)]
        else:
            metaDataFrame = metaDataFrame[(metaDataFrame.classifierPrediction != PlagiarismClass.none.name)]
        return metaDataFrame
    
    def GroupByRawTextPair(self, metaDataFrame):
        return metaDataFrame.groupby([SeedAttributesNames.Names.metaRawTextPair])

    def CastToDetectionGroupsByRawTextPair(self, groupedByRawTextPairMetaDataFrame):
        detectionGroups = []
        for rawTextPair, metaDataFrame in groupedByRawTextPairMetaDataFrame:
            detectionListFromRawTextPair = DetectionListFromRawTextPair(rawTextPair)
            detectionListFromRawTextPair.detectionList = [
                PanExportProcess.CastSeedRawTextPairToDetection(row.metaSeed, rawTextPair)
                for index, row in metaDataFrame.iterrows()]
            detectionGroups.append(detectionListFromRawTextPair)
        return detectionGroups

    def CastSeedRawTextPairToDetection(seed, rawTextPair):
        return Detection(
            name = PanSettings.detectionName,
            obfuscation = None,
            _type = PanSettings._type,
            obfuscationDegree = None,
            isGiven = EnumYesNo.no,
            isDetected = EnumYesNo.yes,
            rawTextSuspiciousLocation = seed.suspiciousSentence.rawTextExcerptLocation,
            rawTextSourceLocation = seed.sourceSentence.rawTextExcerptLocation,
            textCollectionMeta = None,
            rawTextPair = rawTextPair)
    
    def StoreDetectionGroupsByRawTextPair(self, detectionGroupsByRawTextPair):
        for detectionListFromRawTextPair in detectionGroupsByRawTextPair:
            self._panExportRepository.StoreXml(detectionListFromRawTextPair = detectionListFromRawTextPair)

    def __init__(self):
        self._classifierMetaRepository = ClassifierMetaRepository()
        self._panExportRepository = PanExportRepository()
        super().__init__()
