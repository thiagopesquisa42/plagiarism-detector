from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Entity import _EntityBase as EntityBase

class BagOfTexts(EntityBase):
    __tablename__           = 'bag_of_texts'
    id                      = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    textCollectionMetaId    = Column(Integer, ForeignKey('text_collection_meta.id'), nullable=False)
    textCollectionMeta      = relationship('TextCollectionMeta', foreign_keys=[textCollectionMetaId])
    
    #unique identifier of the object
    def __repr__(self):
        return "<BagOfTexts (id='" + id + "'>"
