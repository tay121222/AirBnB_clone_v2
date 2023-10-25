#!/usr/bin/python3
""" City Module for HBNB project
state = relationship("State", back_populates="cities") """
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
import os

class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        # state = relationship("State", back_populates="cities")
        place = relationship("Place", cascade='all, delete, delete-orphan', back_populates="cities")
    else:
        name = ""
        state_id = ""

