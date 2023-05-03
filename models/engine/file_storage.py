#!/usr/bin/python3
"""File Storage module for persisting instances"""

import json
import os


class FileStorage:
    """
    Serializes instances to a JSON file and
    deserializes JSON file to instances
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns all stored instances"""
        if cls is not None:
            reqObjects = {}
            for key, value in self.__objects.items():
                if type(value) == cls:
                    reqObjects[key] = value
            return reqObjects
        else:
            return FileStorage.__objects

    def new(self, obj):
        """
        Saves obj into __objects with the key <obj class name>.id
        """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serializes __objects to file.json"""
        objs = {}
        with open(self.__file_path, 'w') as file:
            for key, value in self.__objects.items():
                objs[key] = value.to_dict()
            json.dump(objs, file)

    def delete(self, obj=None):
        """Deletes obj from __objects"""
        if obj is not None:
            keyToDel = ''
            for key, value in self.__objects.items():
                if obj.to_dict() == value.to_dict():
                    keyToDel = key
            del (self.__objects[keyToDel])

    def class_list(self):
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        return {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
        }

    def reload(self):
        """Deserializes the Json file to __objects"""
        from models.base_model import BaseModel

        json_load = {}
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                json_load = json.load(file)
            for key, value in json_load.items():
                calling_class = self.class_list()[value['__class__']]
                self.__objects[key] = calling_class(**value)
        else:
            return

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
        """Calls reload method to deserialize JSON file"""
        self.reload()
