from sqlalchemy import Column, Integer, String, DateTime
from Entity import _EntityBase as EntityBase

class TextCollectionMeta(EntityBase):
    __tablename__ = 'text_collection_meta'
    id              =   Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    creationDate    =   Column(DateTime, nullable=False)
    name        =   Column(Integer, nullable=False)
    sourceUrl       =   Column(String, nullable=True)
    description     =   Column(String, nullable=False)
    
    #unique identifier of the object
    def __repr__(self):
        return "<TextCollectionMeta (id='" + id + "'>"