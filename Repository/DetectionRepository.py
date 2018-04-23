from Repository import _DataBaseConnection as DataBaseConnection
from Entity import _Detection as Detection

class DetectionRepository(DataBaseConnection):

    def Insert(self, detection):
        if(detection == None):
            return
        self.session.add(detection)
        self.session.commit()

    def Get(self, id):
        return self.session.query(Detection).filter(Detection.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
