from Repository import _BaseRepository as BaseRepository
from Entity.Classifier import _ClassifierMeta as ClassifierMeta

class ClassifierMetaRepository(BaseRepository):
    def Get(self, id):
        return self.session.query(ClassifierMeta).filter(ClassifierMeta.id == id).first()

    def UpdateByRawSql(self, classifierMeta):
        self.engine.execute(
            ClassifierMeta.__table__.update(
                whereclause = "id = " + str(classifierMeta.id)),
                [classifierMeta.ToDictionary()])

    def Hello(self):
        print ('Hello, I\'m a repository')

    def __init__(self):
        super().__init__()
