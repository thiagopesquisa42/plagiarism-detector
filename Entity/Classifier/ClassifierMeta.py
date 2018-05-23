from sqlalchemy import Column, Integer, ForeignKey, BLOB, JSON
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase
import pickle

class ClassifierMeta(EntityBase):
    __tablename__               = 'classifier_meta'
    id                          = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    pickleClassifier            = Column(BLOB, nullable=False)
    definitionDictionary        = Column(JSON, nullable=False)
    seedingDataFrameId          = Column(Integer, ForeignKey('seeding_data_frame.id'), nullable=True)
    seedingDataFrame            = relationship('SeedingDataFrame', foreign_keys=[seedingDataFrameId])
    pickleExpectedPredictedList = Column(BLOB, nullable=False)

    #unique identifier of the object
    def __repr__(self):
        return "<ClassifierMeta (id='" + id + "'>"

    def GetClassifier(self):
        return pickle.loads(self.pickleClassifier)

    def SetPickleClassifier(self, classifier):
        self.pickleClassifier = pickle.dumps(classifier)
    
    def GetExpectedPredictedList(self):
        return pickle.loads(self.pickleExpectedPredictedList)

    def SetPickleExpectedPredictedList(self, expectedPredictedList):
        self.pickleExpectedPredictedList = pickle.dumps(expectedPredictedList)

    def ToDictionary(self):
        return {
            'id':                           self.id,                         
            'pickleClassifier':             self.pickleClassifier,           
            'definitionDictionary':         self.definitionDictionary,       
            'seedingDataFrameId':           self.seedingDataFrameId,         
            'pickleExpectedPredictedList':  self.pickleExpectedPredictedList
        }