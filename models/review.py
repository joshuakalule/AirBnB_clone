#!/usr/bin/python3
"""Class for reviews."""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Class for reviews that inherits from BaseModel.

    Attributes
    ----------
    place_id : str
        empty string
    user_id : str
        empty string
    text : str
        empty string
    """

    place_id = ""
    user_id = ""
    text = ""
