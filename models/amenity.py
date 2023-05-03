#!/usr/bin/python3
"""Amenity model"""


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models.place import place_amenity
from sqlalchemy.orm import relationship
from os import getenv


class Amenity(BaseModel, Base):
    """Amenity class"""
    __tablename__ = "amenities"

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
        place_amenities = []

    def __init__(self, *args, **kwargs):
        """Initializes an Amenity instance"""
        super().__init__(*args, **kwargs)
