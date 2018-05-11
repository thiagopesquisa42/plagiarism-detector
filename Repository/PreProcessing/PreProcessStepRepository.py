from Repository import _BaseRepository as BaseRepository
from Entity.PreProcessing import _PreProcessStep as PreProcessStep

class PreProcessStepRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(PreProcessStep).filter(PreProcessStep.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
