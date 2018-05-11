from Repository import _BaseRepository as BaseRepository
from Entity.PreProcessing import _PreProcessStepChainNode as PreProcessStepChainNode

class PreProcessStepChainNodeRepository(BaseRepository):

    def Get(self, id):
        return self.session.query(PreProcessStepChainNode).filter(PreProcessStepChainNode.id == id).first()

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
