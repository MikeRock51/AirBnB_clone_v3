#!/usr/bin/python3
"""A module containing the base model of my console"""


from uuid import uuid4
from datetime import datetime
# from models import storage
from copy import copy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

Base = declarative_base()


class BaseModel:
    """Defines all common attributes and methods for other classes"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Object contructor"""

        if kwargs and 'id' in kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            if kwargs:
                for key, value in kwargs.items():
                    setattr(self, key, value)

    def __str__(self):
        return ("[{}] ({}) {}".format
                (type(self).__name__, self.id, self.__dict__))

    def delete(self):
        """Deletes the current instance"""
        storage.delete(self)

    def save(self):
        """Updates the updated_at attribute to current time"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Generates a dictionary representation of an instance"""
        instance = copy(self.__dict__)
        instance['__class__'] = type(self).__name__
        instance['created_at'] = instance['created_at'].isoformat()
        instance['updated_at'] = instance['updated_at'].isoformat()
        if '_sa_instance_state' in instance:
            del (instance['_sa_instance_state'])

        return instance
