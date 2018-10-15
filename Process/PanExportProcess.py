from itertools import groupby

from Entity import _Detection as Detection
from Entity import _PlagiarismClass as PlagiarismClass
from Entity import _Detection as Detection
from Entity import _DetectionListFromRawTextPair as DetectionListFromRawTextPair
from Entity import _EnumYesNo as EnumYesNo
from Entity import _Location as Location
from Entity.PreProcessing import _RawTextExcerptLocation as RawTextExcerptLocation
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

            classes = self.GetDetectionClasses(metaDataFrame)
            folderPath_Class_TupleList = []
            for thisClass in classes:
                self.logger.info('keeping only one class')
                thisMetaDataFrame = self.RemoveAllExceptThisClass(metaDataFrame, thisClass)

                self.logger.info('grouping by raw-text-pair')
                groupedByRawTextPairMetaDataFrame = self.GroupByRawTextPair(thisMetaDataFrame)
                
                self.logger.info('cast to detection groups')
                detectionGroups = self.CastToDetectionGroupsByRawTextPair(groupedByRawTextPairMetaDataFrame)

                self.logger.info('fuse adjacent detections per raw text pair')
                detectionGroups = self.FuseAdjacentDetectionPerRawTextPair(detectionGroups)

                self.logger.info('exporting groups')
                folderNickName = str(classifierMeta.GetName()) + '_US_' + str(thisClass)
                folderPath = self._panExportRepository.StoreMultipleXml(detectionGroups, folderNickName)
                folderPath_Class_TupleList.append((folderPath, thisClass))

        except Exception as exception:
            self.logger.exception('[Export Pan Formatted Detections] failure: ' + str(exception))
            raise exception
        else:
            self.logger.info('[Export Pan Formatted Detections] finished')
            return folderPath_Class_TupleList
    
    def GetDetectionClasses(self, metaDataFrame):
        classes = metaDataFrame.plagiarismClass.unique()
        classes = list(filter(lambda c: c not in [False, PlagiarismClass.none, PlagiarismClass.none.name], classes))
        return classes

    def RemoveAllExceptThisClass(self, metaDataFrame, thisClass):
        _metaDataFrame = metaDataFrame[(metaDataFrame.classifierPrediction == thisClass)]
        return _metaDataFrame

    def RemoveNotDetections(self, metaDataFrame):
        classes = metaDataFrame.plagiarismClass.unique()
        if(len(classes) == 2):
            metaDataFrame = metaDataFrame[(metaDataFrame.classifierPrediction == True)]
        else:
            noneClass = PlagiarismClass.none if(PlagiarismClass.none in classes) else PlagiarismClass.none.name
            metaDataFrame = metaDataFrame[(metaDataFrame.classifierPrediction != noneClass)]
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

    def FuseAdjacentDetectionPerRawTextPair(self, detectionGroupsByRawTextPair):
        for detectionListFromRawTextPair in detectionGroupsByRawTextPair:
            locationList = PanExportProcess.CastDetectionListToLocationList(detectionListFromRawTextPair.detectionList)
            locationListFused = PanExportProcess.FuseAdjacentLocations(locationList)
            detectionListFromRawTextPair.detectionList = PanExportProcess.CastLocationListToDetectionList(
                locationListFused, detectionListFromRawTextPair.rawTextPair)
        return detectionGroupsByRawTextPair

    def CastDetectionListToLocationList(detectionList):
        return [
            Location(
                left = detection.rawTextSuspiciousLocation.firstCharacterPosition, 
                right = detection.rawTextSuspiciousLocation.lastCharacterPosition, 
                up = detection.rawTextSourceLocation.firstCharacterPosition,
                down = detection.rawTextSourceLocation.lastCharacterPosition)
            for detection in detectionList]

    def CastLocationListToDetectionList(locationList, rawTextPair):
        return [
            Detection(
                name = PanSettings.detectionName,
                obfuscation = None,
                _type = PanSettings._type,
                obfuscationDegree = None,
                isGiven = EnumYesNo.no,
                isDetected = EnumYesNo.yes,
                rawTextSuspiciousLocation = RawTextExcerptLocation(
                    firstCharacterPosition = location.left,
                    lastCharacterPosition = location.right,
                    stringLength = location.right - location.left,
                    rawText = rawTextPair.suspiciousRawText),
                rawTextSourceLocation = RawTextExcerptLocation(
                    firstCharacterPosition = location.up,
                    lastCharacterPosition = location.down,
                    stringLength = location.down - location.up,
                    rawText = rawTextPair.sourceRawText),
                textCollectionMeta = None,
                rawTextPair = rawTextPair)
            for location in locationList]
    
    def GetLocationMatrixLineUpDownColumnLeftRight(unsortedList):
        sortedListByUpLeft = sorted(unsortedList, key = lambda location: (location.up, location.left))
        matrixSorted = [
            (
                up, down,
                [location for location in listIterator])
            for (up, down), listIterator in groupby(sortedListByUpLeft, lambda location: (location.up, location.down))]
        return matrixSorted

    def GetLocationMatrixLineLeftRightColumnUpDown(unsortedList):
        sortedListByLRUD = sorted(unsortedList, key = lambda location: (location.left, location.right, location.up, location.down))
        matrixSorted = [
            (
                left, right,
                [location for location in listIterator])
            for (left, right), listIterator in groupby(sortedListByLRUD, lambda location: (location.left, location.right))]
        return matrixSorted

    def FuseAdjacentLocations(unsortedLocationList):
        matrixLineUpDownColumnLeftRight = PanExportProcess.GetLocationMatrixLineUpDownColumnLeftRight(unsortedLocationList)
        closedList = []
        for up, down, line in matrixLineUpDownColumnLeftRight:
            processingItem = line[0]
            for location in line[1:]:
                if(processingItem.right + 1 == location.left):
                    processingItem.right = location.right
                else:
                    closedList.append(processingItem)
                    processingItem = location
            closedList.append(processingItem)
        matrixLineLeftRightColumnUpDown = PanExportProcess.GetLocationMatrixLineLeftRightColumnUpDown(closedList)
        closedList = []
        for left, right, line in matrixLineLeftRightColumnUpDown:
            processingItem = line[0]
            for location in line[1:]:
                if(processingItem.down + 1 == location.up):
                    processingItem.down = location.down
                else:
                    closedList.append(processingItem)
                    processingItem = location
            closedList.append(processingItem)
        return closedList

    def StoreDetectionGroupsByRawTextPair(self, detectionGroupsByRawTextPair):
        for detectionListFromRawTextPair in detectionGroupsByRawTextPair:
            self._panExportRepository.StoreXml(detectionListFromRawTextPair = detectionListFromRawTextPair)

    def __init__(self):
        self._classifierMetaRepository = ClassifierMetaRepository()
        self._panExportRepository = PanExportRepository()
        super().__init__()
