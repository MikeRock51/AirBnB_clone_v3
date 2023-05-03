#!/usr/bin/python3
"""The review model"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from os import getenv


class Review(BaseModel, Base):
    """The review class"""
    __tablename__ = "reviews"
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes a Review instance"""
        super().__init__(*args, **kwargs)
