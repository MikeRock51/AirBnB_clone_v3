#!/usr/bin/python3
"""The city model"""


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.place import Place
from os import getenv


class City(BaseModel, Base):
    """The city class"""
    __tablename__ = "cities"

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='cities', cascade='all, delete')
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """Initializes a city instance"""
        super().__init__(*args, **kwargs)
