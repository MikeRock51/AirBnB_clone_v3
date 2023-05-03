#!/usr/bin/python3
"""Defines the database storage engine for the program"""

from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """DB storage engine class"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv('HBNB_MYSQL_USER')
        host = getenv('HBNB_MYSQL_HOST')
        pwd = getenv('HBNB_MYSQL_PWD')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}"
            .format(user, pwd, host, db), pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            from models.base_model import Base
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects from the database"""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        objects = {}
        if cls is not None:
            queryResult = self.__session.query(cls).all()

            for result in queryResult:
                key = "{}.{}".format(result.__class__.__name__, result.id)
                objects[key] = result
        else:
            for className in [City, State, User, Place, Review, Amenity]:
                queryResult = self.__session.query(className).all()
                for result in queryResult:
                    key = "{}.{}".format(result.__class__.__name__, result.id)
                    objects[key] = result
        return objects

    def new(self, obj):
        """Adds obj to the current database session"""
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Creates all tables in the database"""
        from models.base_model import Base
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def get(self, cls, id):
        """Retrieves a single object"""
        objs = self.all(cls)
        for obj in objs.values():
            if obj.id == id:
                return obj
        return None

    def count(self, cls=None):
        """Counts the number of objects in storage"""
        if cls:
            objs = self.all(cls)
        else:
            objs = self.all()
        return len(objs)

    def close(self):
        """Removes the current session"""
        self.__session.remove()
