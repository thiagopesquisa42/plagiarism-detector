from Repository import _BaseRepository as BaseRepository
from Entity import _Detection as Detection

class DetectionRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(Detection).filter(Detection.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
