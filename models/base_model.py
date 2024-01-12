#!/usr/bin/python3
"""
This file contains the BaseModel class that parents all classess
used in the project.
"""
from uuid import uuid4
import datetime
import models


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
        if kwargs:
            self.create_from_dict(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            models.storage.new(self)

    def create_from_dict(self, dictionary):
        """Create BaseModel object from dictionary."""

        for key, value in dictionary.items():
            if key == '__class__':
                pass
            elif key == 'created_at':
                self.created_at = datetime.datetime.fromisoformat(value)
            elif key == 'updated_at':
                self.updated_at = datetime.datetime.fromisoformat(value)
            else:
                setattr(self, key, value)

    def __str__(self):
        """Prints [<class name>] (<self.id>) <self.__dict__>."""

        return (f"[{__class__.__name__}] ({self.id}) {self.__dict__}")

    def save(self):
        """
        Updates the public instance attribute updated_at with the current
        datetime.
        Saves to file using storage obj <type - FileStorage>
        """

        self.updated_at = datetime.datetime.now()
        models.storage.save()

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
