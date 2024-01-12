#!/usr/bin/python3
"""Class for places."""

from models.base_model import BaseModel


class Place(BaseModel):
    """
    Class for places that inherits from BaseModel

    Attributes
    ----------
    city_id : str
        empty string
    user_id : str
        empty string
    name : str
        empty string
    description : str
        empty string
    number_rooms : int
        0 (zero)
    number_bathrooms : int
        0 (zero)
    max_guest : int
        0 (zero)
    price_by_night : int
        0 (zero)
    latitude : float
        0.0
    longitude : float
        0.0
    amenity_ids : list
        list of strings
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = list()
