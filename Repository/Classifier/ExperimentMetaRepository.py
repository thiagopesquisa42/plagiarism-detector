from Repository import _BaseRepository as BaseRepository
from datetime import datetime
import os

class ExperimentMetaRepository(BaseRepository):
    name = 'ExperimentMetaRepository'

    def GetReportUniqueName(self):
        dateTimeString = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(self.rootLocation, self.name + dateTimeString + '.txt')

    def GetReportWriter(self):
        reportName = self.GetReportUniqueName()
        return open(reportName, 'w')

    def StoreReport(self, report):
        try:
            fileWriter = self.GetReportWriter()
            buffer = str(report)
            fileWriter.write(buffer)
        except Exception as exception:
            self.logger.info('failure when storing item, error ' + str(exception))
        else:
            self.logger.info('item stored: ' + str(type(report)))
            return fileWriter.name

    def __init__(self):
        super().__init__()
        rootLocation = os.path.join(self.rootLocation, self.name)
