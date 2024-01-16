#!/usr/bin/python3
"""
Unittest for place.py.
"""

import unittest
import datetime
from datetime import datetime as dt
import re
import os

from models.place import Place
from models.engine.file_storage import FileStorage

test_path = "_tmp_path_1.json"
memory_path = "_tmp_path_memory.json"


class TestBase(unittest.TestCase):
    """Base test class for tests for the Place class."""

    @classmethod
    def setUpClass(cls):
        """
        store name of FileStorage.__file_path
        Keep copy of FileStorage.__file_path contents
        set FileStorage.__file_path to test_path
        """
        cls.original_path = FileStorage._FileStorage__file_path
        if os.path.exists(cls.original_path):
            with open(cls.original_path, 'r') as fp_from:
                with open(memory_path, 'w') as fp_to:
                    fp_to.write(fp_from.read())
        FileStorage._FileStorage__file_path = test_path

    @classmethod
    def tearDownClass(cls):
        """
        rm test_path
        copy back contents of FileStorage.__file_path
        rm memory_path
        reset FileStorage.__file_path to original path
        """
        if os.path.exists(test_path):
            os.remove(test_path)
        if os.path.exists(memory_path):
            with open(memory_path, 'r') as from_fp:
                with open(cls.original_path, 'w') as to_fp:
                    to_fp.write(from_fp.read())
            os.remove(memory_path)
        FileStorage._FileStorage__file_path = cls.original_path

    def setUp(self):
        """Create Place obj."""
        self.obj = Place()

    def tearDown(self):
        """Delete Place obj."""
        del self.obj


class TestPlaceAttributes(TestBase):
    """Test Place attributes."""

    def test_id(self):
        """Check that id attribte is a string."""
        self.assertIsInstance(self.obj.id, str)

    def test_created_at(self):
        """Check that created_at attribute is a datetime object."""
        self.assertIsInstance(self.obj.created_at, dt)

    def test_updated_at(self):
        """Check that updated_at attribute is a datetime object."""
        self.assertIsInstance(self.obj.updated_at, dt)

    def test_city_id(self):
        """Check that city_id attribute is a str object."""
        if hasattr(self.obj, 'city_id'):
            self.assertIsInstance(self.obj.city_id, str)

    def test_user_id(self):
        """Check that user_id attribute is a str object."""
        if hasattr(self.obj, 'user_id'):
            self.assertIsInstance(self.obj.user_id, str)

    def test_name(self):
        """Check that name attribute is a str object."""
        if hasattr(self.obj, 'name'):
            self.assertIsInstance(self.obj.name, str)

    def test_description(self):
        """Check that description attribute is a str object."""
        if hasattr(self.obj, 'description'):
            self.assertIsInstance(self.obj.description, str)

    def test_number_rooms(self):
        """Check that number_rooms attribute is an int object."""
        if hasattr(self.obj, 'number_rooms'):
            self.assertIsInstance(self.obj.number_rooms, int)

    def test_number_bathrooms(self):
        """Check that number_bathrooms attribute is an int object."""
        if hasattr(self.obj, 'number_bathrooms'):
            self.assertIsInstance(self.obj.number_bathrooms, int)

    def test_max_guest(self):
        """Check that max_guest attribute is an int object."""
        if hasattr(self.obj, 'max_guest'):
            self.assertIsInstance(self.obj.max_guest, int)

    def test_price_by_night(self):
        """Check that price_by_night attribute is an int object."""
        if hasattr(self.obj, 'price_by_night'):
            self.assertIsInstance(self.obj.price_by_night, int)

    def test_latitude(self):
        """Check that latitude attribute is a float object."""
        if hasattr(self.obj, 'latitude'):
            self.assertIsInstance(self.obj.latitude, float)

    def test_longitude(self):
        """Check that longitude attribute is a float object."""
        if hasattr(self.obj, 'longitude'):
            self.assertIsInstance(self.obj.longitude, float)

    def test_amenity_ids(self):
        """Check that amenity_ids attribute is a list of strings."""
        if not hasattr(self.obj, 'amenity_ids'):
            return
        self.assertIsInstance(self.obj.amenity_ids, list)

        for amenity_id in self.obj.amenity_ids:
            self.assertIsInstance(amenity_id, str)


class TestPlacestrMethod(TestBase):
    """Test the Place.str() method."""

    def test___str__(self):
        """Check that the __str__() method returns a str type."""
        self.assertIsInstance(self.obj.__str__(), str)

    def test___str__class_name(self):
        """
        Check that the class name in __str__ conforms to the format;
        [<class name>]
        Check that the class name in __str__ matches the class name of
        the object
        """
        regex = r"^\[(\w+)\]\s"
        self.assertRegex(self.obj.__str__(), regex)
        if (m := re.search(regex, self.obj.__str__())):
            class_name = m.group(1)
            self.assertEqual(class_name, self.obj.__class__.__name__,
                             msg=f"""[{class_name}] does not match
                             '{type(self.obj).__name__}'""")

    def test__str__id(self):
        """
        Check that the id in __str__ conforms to the format; (<self.id>)
        Check that the id in __str__ matches the id from the object
        """
        regex = r"\s\(([-a-zA-Z0-9]+)\)\s"
        self.assertRegex(self.obj.__str__(), regex)
        if (m := re.search(regex, self.obj.__str__())):
            _id = m.group(1)
            self.assertEqual(_id, self.obj.id,
                             msg=f"({_id}) does not match 'self.obj.id'")

    def test__str__dict(self):
        """
        Check that the dictionary in __str__ conforms to the format;
        <self.__dict__>
        Check that the dictionary matches instance dictionary
        """
        regex = "({.+})$"
        self.assertRegex(self.obj.__str__(), regex)
        if (m := re.search(regex, self.obj.__str__())):
            _dict_str = m.group(1)
            _dict = eval(_dict_str)
            self.assertIsInstance(_dict, dict,
                                  msg=f'''__str__ dict is not a
                                  dictionary obj''')
            if (isinstance(_dict, dict)):
                self.assertDictEqual(_dict, self.obj.__dict__,
                                     msg=f'''dict in __str__ does not equal
                                     self.__dict__''')


class TestPlacesaveMethod(TestBase):
    """Test the Place.save() method."""

    def test_change_updated_at(self):
        """Check that updated_at attribute changes when save() is executed."""
        before = self.obj.updated_at
        self.obj.save()
        self.assertNotEqual(before, self.obj.updated_at)


class TestPlaceToDictMethod(TestBase):
    """Test the to_dict() method."""

    def test_output(self):
        """Check that the output is a dictionary type."""
        self.assertIsInstance(self.obj.to_dict(), dict)

    def test__class__key(self):
        """Check that the key '__class__' exists in the return."""
        _dict = self.obj.to_dict()
        self.assertTrue('__class__' in _dict)
        if '__class__' in _dict:
            self.assertEqual(_dict['__class__'], self.obj.__class__.__name__)

    def test_has__dict__items(self):
        """
        Check that all key/value pairs in instance.__dict__ reflect in
        the return
        """
        _dict = self.obj.to_dict()
        for key in self.obj.__dict__:
            self.assertTrue(key in _dict)

    def test_created_at(self):
        """
        Check that the value of created_at in the return is of a
        string type
        Check that created_at from the return matches that of the instance
        """
        _dict = self.obj.to_dict()
        created_at = _dict['created_at']
        self.assertIsInstance(created_at, str)
        try:
            datetime_obj = dt.fromisoformat(created_at)
            self.assertEqual(datetime_obj, self.obj.created_at)
        except Exception as e:
            e_name = e.__class__.__name__
            self.fail(msg=f"{e_name} raised when converting from isoformat")

    def test_updated_at(self):
        """
        Check that the value of updated_at in the return is of a
        string type
        Check that updated_at from the return matches that of the instance
        """
        _dict = self.obj.to_dict()
        updated_at = _dict['updated_at']
        self.assertIsInstance(updated_at, str)
        try:
            datetime_obj = dt.fromisoformat(updated_at)
            self.assertEqual(datetime_obj, self.obj.updated_at)
        except Exception as e:
            e_name = e.__class__.__name__
            self.fail(msg=f"{e_name} raised when converting from isoformat")


class TestPlaceCreateFromDict(TestBase):
    """Test objects created from kwargs (dictionary)."""

    @classmethod
    def setUpClass(cls):
        """Create dummy dict."""
        super().setUpClass()
        cls.place_dict = {
            '__class__': 'Place',
            'id': '68940dfc-901f-4af2-93df-e05490bea019',
            'created_at': '2024-01-10T01:54:23.523307',
            'updated_at': '2024-01-10T01:54:23.523376'
        }
        cls.other_attrs = {
            'city_id': '6k940cfc-901f-4ak2-93df-e0a490bea019',
            'user_id': '6k94ryfc-901f-4902-93df-e0a490ffa019',
            'name': 'Home',
            'description': 'Where food is free',
            'number_rooms': 3,
            'number_bathrooms': 3,
            'max_guest': 1,
            'price_by_night': 150000,
            'latititude': -1.00,
            'longitude': 37.00,
            'amenity_ids': ['121212', '141414', '191919']
        }
        cls.all_dict = {**cls.place_dict, **cls.other_attrs}

    def setUp(self):
        """Create custom Place dict."""
        super().setUp()
        self.obj = Place(**self.__class__.all_dict)

    def test_same_class(self):
        """Check that the new object has the same class name as the kwargs."""
        self.assertEqual(self.obj.__class__, Place)

    def test_same_id(self):
        """Check that the new obj id matches that in the dictionary."""
        self.assertEqual(self.obj.id, '68940dfc-901f-4af2-93df-e05490bea019')

    def test_same_created_at(self):
        """Check that created_at matches that in the dictionary."""
        dt_created_at = dt.fromisoformat("2024-01-10T01:54:23.523307")
        self.assertEqual(self.obj.created_at, dt_created_at)

    def test_same_updated_at(self):
        """Check that updated_at matches that in the dictionary."""
        dt_updated_at = dt.fromisoformat("2024-01-10T01:54:23.523376")
        self.assertEqual(self.obj.updated_at, dt_updated_at)

    def test_other_attributes(self):
        """
        Check that other attributes from the dictionary reflect in
        the new object
        """
        _dict = TestPlaceCreateFromDict.other_attrs
        for key, value in _dict.items():
            obj_attr = eval(f"self.obj.{key}")
            self.assertTrue(type(_dict[key]) is type(obj_attr),
                            msg="type(dict_attr) does not match\
                            type(obj_attr)")
            self.assertEqual(_dict[key], obj_attr)
