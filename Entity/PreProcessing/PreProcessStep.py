from sqlalchemy import Column, Integer, ForeignKey, Enum, String, JSON
from Entity import _EntityBase as EntityBase

class PreProcessStep(EntityBase):
    __tablename__                   = 'pre_process_step'
    id                              = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    algorithm                       = Column(JSON, nullable=False)

    #unique identifier of the object
    def __repr__(self):
        return "<PreProcessStep id='" + id + "'>"

