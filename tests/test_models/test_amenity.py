#!/usr/bin/python3
"""
Unittest for amenity.py.
"""

import unittest
import datetime
from datetime import datetime as dt
import re
import os

from models.amenity import Amenity
from models.engine.file_storage import FileStorage

test_path = "_tmp_path_1.json"
memory_path = "_tmp_path_memory.json"


class TestBase(unittest.TestCase):
    """Base test class for tests for the Amenity class."""

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
        """Create Amenity obj."""
        self.obj = Amenity()

    def tearDown(self):
        """Delete Amenity obj."""
        del self.obj


class TestAmenityAttributes(TestBase):
    """Test Amenity attributes."""

    def test_id(self):
        """Check that id attribte is a string."""
        self.assertIsInstance(self.obj.id, str)

    def test_created_at(self):
        """Check that created_at attribute is a datetime object."""
        self.assertIsInstance(self.obj.created_at, dt)

    def test_updated_at(self):
        """Check that updated_at attribute is a datetime object."""
        self.assertIsInstance(self.obj.updated_at, dt)

    def test_name(self):
        """Check that name attribute is a str object."""
        if hasattr(self, 'name'):
            self.assertIsInstance(self.obj.name, str)


class TestAmenitystrMethod(TestBase):
    """Test the Amenity.str() method."""

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


class TestAmenitysaveMethod(TestBase):
    """Test the Amenity.save() method."""

    def test_change_updated_at(self):
        """Check that updated_at attribute changes when save() is executed."""
        before = self.obj.updated_at
        self.obj.save()
        self.assertNotEqual(before, self.obj.updated_at)


class TestAmenityToDictMethod(TestBase):
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


class TestAmenityCreateFromDict(TestBase):
    """Test objects created from kwargs (dictionary)."""

    @classmethod
    def setUpClass(cls):
        """Create dummy dict."""
        super().setUpClass()
        cls.amenity_dict = {
            '__class__': 'Amenity',
            'id': '68940dfc-901f-4af2-93df-e05490bea019',
            'created_at': '2024-01-10T01:54:23.523307',
            'updated_at': '2024-01-10T01:54:23.523376'
        }
        cls.other_attrs = {
            'name': 'Amenity_1'
        }
        cls.all_dict = {**cls.amenity_dict, **cls.other_attrs}

    def setUp(self):
        """Create custom Amenity dict."""
        super().setUp()
        self.obj = Amenity(**self.__class__.all_dict)

    def test_same_class(self):
        """Check that the new object has the same class name as the kwargs."""
        self.assertEqual(self.obj.__class__, Amenity)

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
        _dict = TestAmenityCreateFromDict.other_attrs
        for key, value in _dict.items():
            obj_attr = eval(f"self.obj.{key}")
            self.assertTrue(type(_dict[key]) is type(obj_attr),
                            msg="type(dict_attr) does not match\
                            type(obj_attr)")
            self.assertEqual(_dict[key], obj_attr)
