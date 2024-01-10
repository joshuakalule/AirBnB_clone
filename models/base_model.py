#!/usr/bin/python3
"""
This file contains the BaseModel class that parents all classess
used in the project.
"""
from uuid import uuid4
import datetime


class BaseModel:
    """
    Defines all common attributes/methods for other classes.

    Attributes
    ----------
    id : string
    unique idententifier
    created_at : datetime.datetime
    date and time of creation
    updated_at : datetime.datetime
    date and time when instance was last modified
    """

    def __init__(self, *args, **kwargs):
        if len(kwargs) == 0:
            self.id = str(uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
        else:
            self.create_from_dict(kwargs)

    def create_from_dict(self, dictionary):
        """Create Base model from dictionary."""

        for key, value in dictionary.items():
            if key == '__class__':
                pass
            elif key == 'created_at':
                self.created_at = datetime.datetime.fromisoformat(value)
            elif key == 'updated_at':
                self.updated_at = datetime.datetime.fromisoformat(value)
            else:
                if isinstance(value, str):
                    exec(f"self.{key} = '{value}'")
                else:
                    exec(f"self.{key} = {value}")

    def __str__(self):
        """Prints [<class name>] (<self.id>) <self.__dict__>."""

        return (f"[{__class__.__name__}] ({self.id}) {self.__dict__}")

    def save(self):
        """
        Updates the public instance attribute updated_at with the current
        datetime.
        """

        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__
        of the instance.
        """
        model_dict = self.__dict__.copy()
        model_dict["__class__"] = self.__class__.__name__
        model_dict["created_at"] = self.created_at.isoformat()
        model_dict["updated_at"] = self.updated_at.isoformat()
        return model_dict
