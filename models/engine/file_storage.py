#!/usr/bin/python3
"""Handles File storage."""

import json
import os.path


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

    __file_path = str()
    __objects = dict()

    def all(self):
        """Returns the dictionary FileStorage.__objects."""

        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""

        class_name = obj.__class__.name
        _id = obj.id

        key = f'{class_name}.{_id}'

        FileStorage.__objects.update({key: obj.to_dict()})

    def save(self):
        """Serializes __objects to the JSON file."""

        with open(__file_path, 'w') as fp:
            json.dump(FileStorage.__objects, fp)

    def reload(self):
        """Deserializes the JSON file to __objects."""

        if os.path.exists(__file_path):
            with open(__file_path, 'r') as fp:
                FileStorage.__objects = json.load(fp)
