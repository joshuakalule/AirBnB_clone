#!/usr/bin/python3

"""Contains test Files for the file_storage.py file."""

import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel

class BaseCase(unittest.TestCase):
    """Base class for all classes."""

    def setUp(self):
        self.file_storage_obj = FileStorage()

    def teardown(self):
        del self.file_storage_obj


class TestFileStorageAllMethod(BaseCase):
    """Tests the Filestorage.all() method."""

    def test_all_return(self):
        self.assertEqual(self.file_storage_obj.all(), FileStorage.__objects)


class TestFileStorageNewMethod(BaseCase):
    """Tests the FileStorage.new() method."""

    def setUp(self):
        super().setUp()
        self.base_model_obj = BaseModel()
        self.old__objects = FileStorage.__objects

    def tearDown(self):
        super().tearDown()
        del self.model_obj

    def test_dictionary_update_1(self):
        self.obj.new(self.model_obj)
        # __objects should be not be the same
        self.assertNotEqual(old__objects, FileStorage.__objects)
