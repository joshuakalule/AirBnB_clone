#!/usr/bin/python3
"""Handles File storage."""

import json
import os.path
from models.base_model import BaseModel


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file to
    instances

    Attributes
    ----------
    __file_path : string
        path to the JSON file
    __objects : dictionary
        store all objects by <class name>.id
    """

    __file_path = "file.json"
    __objects = dict()

    def all(self):
        """Returns the dictionary FileStorage.__objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        class_name = obj.__class__.__name__
        _id = obj.id
        key = class_name + "." + _id
        value = obj
        FileStorage.__objects.update({key: value})

    def save(self):
        """Serializes __objects to the JSON file."""
        temp_dict = dict()
        for key, obj in FileStorage.__objects.items():
            temp_dict[key] = obj.to_dict()
        with open(FileStorage.__file_path, 'w') as fp:
            json.dump(temp_dict, fp)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        temp_dict = dict()
        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r') as fp:
                temp_dict = json.load(fp)
        for key, _dict in temp_dict.items():
            _class = globals().get(_dict['__class__'])
            FileStorage.__objects[key] = _class(**_dict)
