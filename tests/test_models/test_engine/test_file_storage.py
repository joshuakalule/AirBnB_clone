#!/usr/bin/python3

"""Contains test Files for the file_storage.py file."""

import unittest
import re
import os
import json
import random
import uuid
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

test_path = "_tmp_path.json"
CLASSES = ['BaseModel', 'User', 'State', 'City', 'Amenity', 'Place', 'Review']


class BaseCase(unittest.TestCase):
    """Base class for all classes."""

    @classmethod
    def setUpClass(cls):
        """
        Create copy of __objects
        Clear __objects
        Create copy of __file_path
        Set location for __file_path for tests
        """

        cls.memory__objects = FileStorage._FileStorage__objects.copy()
        FileStorage._FileStorage__objects.clear()

        cls.memory__file_path = FileStorage._FileStorage__file_path
        FileStorage._FileStorage__file_path = test_path

    @classmethod
    def tearDownClass(cls):
        """
        Reset __file_path
        Reset __objects
        rm test_path
        """
        FileStorage._FileStorage__file_path = cls.memory__file_path
        FileStorage._FileStorage__objects = cls.memory__objects.copy()
        if os.path.exists(test_path):
            os.remove(test_path)

    def setUp(self):
        """Pre-prep the FileStorage object for each test."""
        self.file_storage_obj = FileStorage()

    def teardown(self):
        """
        Delete the FileStorage object.
        rm test_path
        """
        del self.file_storage_obj
        if os.path.exists(test_path):
            os.remove(test_path)


class TestFileStorageAllMethod(BaseCase):
    """Tests the Filestorage.all() method."""

    def test_all_return(self):
        """Tests that the all() method returns __objects."""
        all_return = self.file_storage_obj.all()
        __objects = self.file_storage_obj._FileStorage__objects
        self.assertEqual(all_return, __objects)


class TestFileStorageNewMethod(BaseCase):
    """Tests the FileStorage.new() method."""

    def setUp(self):
        """
        Creates a copy of __objects attribute
        Creates a FileStorage obj
        Creates a BaseModel obj
        Runs obj.new() with BaseModel obj as a parameter
        Create copy of new __objects attribute
        """
        self.old__objects = FileStorage._FileStorage__objects.copy()
        super().setUp()
        self.base_model_obj = BaseModel()
        self.file_storage_obj.new(self.base_model_obj)
        self.new__objects = self.file_storage_obj._FileStorage__objects.copy()
        self.key_regex = r"^(\w+)\.([-a-zA-Z0-9]+)$"

    def tearDown(self):
        """
        Clear FileStorage.__objects attr
        Deletes FileStorage obj
        Deletes BaseModel obj
        Deletes old__objects
        Deletes new__objects
        """
        FileStorage._FileStorage__objects.clear()
        super().tearDown()
        del self.base_model_obj
        del self.old__objects
        del self.new__objects

    def test__updates_key_format(self):
        """
        Check that all keys in __updates attr are of the format;
        <class name>.id
        """
        for key in FileStorage._FileStorage__objects:
            self.assertRegex(key, self.key_regex)

    def test__updates_key(self):
        """
        Check that the key added to __objects attribute conforms to
        <obj class name>.id
        """
        if (m := re.search(self.key_regex, list(self.new__objects.keys())[0])):
            class_name = m.group(1)
            _id = m.group(2)
            self.assertEqual(self.base_model_obj.__class__.__name__,
                             class_name)
            self.assertEqual(self.base_model_obj.id, _id)
            self.assertEqual(self.base_model_obj.__class__.__name__,
                             class_name)

    def test__updates_change(self):
        """Checks that __objects changes after new() is called."""
        self.assertNotEqual(self.old__objects, self.new__objects)

    def test__update_plus_1(self):
        """Checks that __objects has 1 extra key/value pair."""
        old_len = len(self.old__objects)
        new_len = len(self.new__objects)
        self.assertEqual(new_len - old_len, 1)


class TestFileStorageSaveMethod(BaseCase):
    """Test the save() method."""

    def setUp(self):
        """
        Inject key/value pair into __objects
        """
        super().setUp()
        base_model_obj = BaseModel()
        key = f"BaseModel.{base_model_obj.id}"
        FileStorage._FileStorage__objects[key] = base_model_obj
        self.injected_obj = base_model_obj

    def tearDown(self):
        """
        Clear __objects
        Delete injected_obj
        """
        super().tearDown()
        FileStorage._FileStorage__objects.clear()
        del self.injected_obj

    def test_serialization(self):
        """
        Check that the object serialized into __file_path
        is the injected object
        """
        self.file_storage_obj.save()

        dict_from_json = dict()
        with open(test_path, 'r') as fp:
            dict_from_json = json.load(fp)

        if dict_from_json:
            injected_id = self.injected_obj.id
            injected_classname = self.injected_obj.__class__.__name__
            injected_key = "{}.{}".format(injected_classname, injected_id)

            self.assertIn(injected_key, dict_from_json,
                          msg="injected key not in dict_from_json")

            """
            Check that the injected key maps to the same dict as that
            from the injected object.
            """
            if (injected_key in dict_from_json):
                injected_dict = self.injected_obj.to_dict()
                retrieved_dict = dict_from_json[injected_key]
                self.assertEqual(injected_dict, retrieved_dict,
                                 msg="""injected dict does not match
                                 retrieved dict""")
        else:
            self.fail("json.loads returns empty dictionary")


class TestFileStorageReloadMethod(BaseCase):
    """Test reload() method."""

    def setUp(self):
        """
        Set injected key
        Set injected dict
        Inject dummy object in test_path
        """
        super().setUp()
        """
        1.create list of objects to test (TOP)
        2.create a list of keys, and dicts
        3.populate the filepath with the keys & dicts to look like contents
            saved in .json file.
        """
        self.injected_items = dict()
        for _class in CLASSES:
            _id = uuid.uuid4()
            key = f"{_class}.{_id}"
            _dict = {
                "__class__": "{}".format(_class),
                "id": "{}".format(_id),
                "updated_at": "2017-09-28T21:07:25.047381",
                "created_at": "2017-09-28T21:07:25.047372",
                "integer": 89,
                "string": "Our string",
                "float": 24.8,
                "list": [
                    str(uuid.uuid4()),
                    str(uuid.uuid4()),
                    str(uuid.uuid4())
                ]
            }

            self.injected_items[key] = _dict

        with open(test_path, 'w') as fp:
            json.dump(self.injected_items, fp)

    def test__objects_updates(self):
        """Check that __objects updates when reload() is executed."""
        before = FileStorage._FileStorage__objects.copy()
        self.file_storage_obj.reload()
        after = FileStorage._FileStorage__objects
        self.assertNotEqual(before, after,
                            msg="__updates dict same as before reload")

    def test_reload_obj_key(self):
        """Check that injected object keys exist in __objects."""
        self.file_storage_obj.reload()
        for key in self.injected_items:
            self.assertIn(key, FileStorage._FileStorage__objects)

    def test_reload_obj_dict(self):
        """Check that the injected obj dict reflects in __objects."""
        self.file_storage_obj.reload()
        """
        4.loop through list of keys
        """
        for key, _dict in self.injected_items.items():
            if key in FileStorage._FileStorage__objects:
                retrieved_obj = FileStorage._FileStorage__objects[key]
                self.assertEqual(_dict, retrieved_obj.to_dict())
