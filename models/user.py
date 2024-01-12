#!/usr/bin/python3
"""Class for Users."""

from models.base_model import BaseModel


class User(BaseModel):
    """
    Class for users that inherits from BaseModel.

    Attributes
    ----------
    email : str
        empty string
    password : str
        empty string
    first_name : str
        empty string
    last_name : str
        empty string
    """
    
    email = ""
    password = ""
    first_name = ""
    last_name = ""
