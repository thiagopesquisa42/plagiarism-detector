from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase
from Entity import _TextCollectionMetaPurpose as TextCollectionMetaPurpose

class TextCollectionMeta(EntityBase):
    __tablename__ = 'text_collection_meta'
    id                          =   Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    creationDate                =   Column(DateTime, nullable=False)
    name                        =   Column(Integer, nullable=False)
    sourceUrl                   =   Column(String, nullable=True)
    description                 =   Column(String, nullable=False)

    purpose                     = Column(Enum(TextCollectionMetaPurpose), nullable=False)
    testTextCollectionMetaId    = Column(Integer, ForeignKey('text_collection_meta.id'), nullable=True)
    testTextCollectionMeta      = relationship('TextCollectionMeta', remote_side=[id])

    #unique identifier of the object
    def __repr__(self):
        return "<TextCollectionMeta (id='" + id + "'>"