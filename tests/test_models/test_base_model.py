#!/usr/bin/python3
"""
Unittest for base_model.py.
"""

import unittest
import datetime
from datetime import datetime as dt
import re

from models.base_model import BaseModel


class TestBase(unittest.TestCase):
    """Base test class for tests fr the BaseModel class."""

    def setUp(self):
        self.obj = BaseModel()

    def tearDown(self):
        del self.obj


class TestBaseModelAttributes(TestBase):

    def test_id(self):
        self.assertIsInstance(self.obj.id, str)

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, dt)

    def test_updated_at(self):
        self.assertIsInstance(self.obj.updated_at, dt)


class TestBaseModelstrMethod(TestBase):

    def test___str__(self):
        self.assertIsInstance(self.obj.__str__(), str)

    def test___str__class_name(self):
        # [<class name>]
        regex = r"^\[(\w+)\]\s"
        self.assertRegex(self.obj.__str__(), regex)
        if (m := re.search(regex, self.obj.__str__())):
            class_name = m.group(1)
            self.assertEqual(class_name, self.obj.__class__.__name__,
                             msg=f"""[{class_name}] does not match
                             '{type(self.obj).__name__}'""")

    def test__str__id(self):
        # (<self.id>)
        regex = r"\s\(([-a-zA-Z0-9]+)\)\s"
        self.assertRegex(self.obj.__str__(), regex)
        if (m := re.search(regex, self.obj.__str__())):
            _id = m.group(1)
            self.assertEqual(_id, self.obj.id,
                             msg=f"({_id}) does not match 'self.obj.id'")

    def test__str__dict(self):
        # <self.__dict__>
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


class TestBaseModelsaveMethod(TestBase):

    def test_change_updated_at(self):
        before = self.obj.updated_at
        self.obj.save()
        self.assertNotEqual(before, self.obj.updated_at)


class TestBaseModelToDictMethod(TestBase):

    def test_output(self):
        self.assertIsInstance(self.obj.to_dict(), dict)

    def test__class__key(self):
        _dict = self.obj.to_dict()
        self.assertTrue('__class__' in _dict)
        if '__class__' in _dict:
            self.assertEqual(_dict['__class__'], self.obj.__class__.__name__)

    def test_has__dict__items(self):
        _dict = self.obj.to_dict()
        for key in self.obj.__dict__:
            self.assertTrue(key in _dict)

    def test_created_at(self):
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
        _dict = self.obj.to_dict()
        updated_at = _dict['updated_at']
        self.assertIsInstance(updated_at, str)
        try:
            datetime_obj = dt.fromisoformat(updated_at)
            self.assertEqual(datetime_obj, self.obj.updated_at)
        except Exception as e:
            e_name = e.__class__.__name__
            self.fail(msg=f"{e_name} raised when converting from isoformat")


class TestBaseModelCreateFromDict(TestBase):

    @classmethod
    def setUpClass(cls):
        cls.base_model_dict = {
            '__class__': 'BaseModel',
            'id': '68940dfc-901f-4af2-93df-e05490bea019',
            'created_at': '2024-01-10T01:54:23.523307',
            'updated_at': '2024-01-10T01:54:23.523376'
        }
        cls.other_attrs = {
            'my_number': 89,
            'name': 'My_First_Model'
        }
        cls.all_dict = {**cls.base_model_dict, **cls.other_attrs}

    def setUp(self):
        self.obj = BaseModel(**self.__class__.all_dict)

    def test_same_class(self):
        self.assertEqual(self.obj.__class__, BaseModel)

    def test_same_id(self):
        self.assertEqual(self.obj.id, '68940dfc-901f-4af2-93df-e05490bea019')

    def test_same_created_at(self):
        dt_created_at = dt.fromisoformat("2024-01-10T01:54:23.523307")
        self.assertEqual(self.obj.created_at, dt_created_at)

    def test_same_updated_at(self):
        dt_updated_at = dt.fromisoformat("2024-01-10T01:54:23.523376")
        self.assertEqual(self.obj.updated_at, dt_updated_at)

    def test_other_attributes(self):
        _dict = TestBaseModelCreateFromDict.other_attrs
        for key, value in _dict.items():
            obj_attr = eval(f"self.obj.{key}")
            self.assertTrue(type(_dict[key]) is type(obj_attr),
                            msg="type(dict_attr) does not match\
                            type(obj_attr)")
            self.assertEqual(_dict[key], obj_attr)
