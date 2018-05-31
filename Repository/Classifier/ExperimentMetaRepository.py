from Repository import _BaseRepository as BaseRepository
from constant import Contexts
from datetime import datetime
import os

class ExperimentMetaRepository(BaseRepository):

    def GetReportUniqueName(self):
        dateTimeString = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(self.GetPath(), self.name + dateTimeString + '.txt')

    def GetReportWriter(self):
        reportName = self.GetReportUniqueName()
        return open(reportName, 'w')

    def StoreReport(self, report):
        try:
            fileWriter = self.GetReportWriter()
            buffer = str(report)
            fileWriter.write(buffer)
        except Exception as exception:
            self.logger.exception('failure when storing item, error ' + str(exception))
            raise exception
        else:
            itemMessage = str(type(report)) + ' fileName: ' + str(fileWriter.name)
            self.logger.info('item stored: ' + itemMessage)
            return fileWriter.name

    def __init__(self):
        super().__init__(context = Contexts.META, name = 'ExperimentMeta')
