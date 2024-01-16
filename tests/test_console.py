#!/usr/bin/python3
"""Tests for console.py."""

import os
import unittest
import json
from unittest.mock import patch, MagicMock
from io import StringIO
from console import HBNBCommand
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from tests import CLASSES

test_path = "_tmp_path.json"
PROMPT_STR = "(hbnb) "
patch.TEST_PREFIX = 'test_'


class BaseCase(unittest.TestCase):
    """Base Test Case for all tests."""

    @classmethod
    def setUpClass(cls):
        """
        copy HBNBCommand().onecmd method
        Create copy of __objects
        Clear __objects
        Create copy of __file_path
        Set location for __file_path for tests
        """
        cls.onecmd = HBNBCommand().onecmd

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

    def teardown(self):
        """
        clear FileStorage.__objects
        rm test_path
        """
        FileStorage._FileStorage__objects.clear()
        if os.path.exists(test_path):
            os.remove(test_path)


class TestConsoleAttributes(BaseCase):
    """Test console attributes."""

    def test_prompt(self):
        """Check that the prompt is PROMPT_STR."""
        self.assertEqual(PROMPT_STR, HBNBCommand.prompt)


class TestUpdateCommand(BaseCase):
    """Test update command."""

    def test_advanced_update_dictionary(self):
        """
        Check that each key/value pair in dict reflects in the
        __objects dict
        when calling <classname>.update(<id> <dictionary>)
        """
        attr_dict = {
            'integer': 23,
            'float': 8.9,
            'list': ['id_0', 'id_1', 'id_2'],
            'string': 'Hello world',
            'string_spaces': 'String with spaces'
        }

        for _class in CLASSES:
            obj = eval(f"{_class}()")
            key = f"{_class}.{obj.id}"

            _dict_str = json.dumps(attr_dict)
            self.onecmd(f"{_class}.update({obj.id}, {_dict_str})")

            __objects = FileStorage._FileStorage__objects
            if key not in __objects:
                return
            fetched_obj = __objects[key]

            for attr_name, attr_value in attr_dict.items():
                msg = f"\nattribute '{attr_name}' in {attr_dict} not found"
                msg += f"\n\nfetched_obj: {fetched_obj.to_dict()}"
                self.assertTrue(hasattr(fetched_obj, attr_name), msg=msg)

                if hasattr(fetched_obj, attr_name):
                    msg = f"attribute {attr_name} was not updated"
                    self.assertEqual(getattr(fetched_obj, attr_name),
                                     attr_value, msg=msg)

    def test_advanced_update_key_value(self):
        """
        check that key/value pair reflects in the __objects dict
        when calling <classname>.update(<id> <attr_name> <attr_value>)
        """
        attr_name = 'xyz'
        attr_value = 'Test value'

        for _class in CLASSES:
            obj = eval(f"{_class}()")
            key = f"{_class}.{obj.id}"

            _cmd = f"{_class}.update({obj.id}, {attr_name}, '{attr_value}')"
            self.onecmd(_cmd)

            __objects = FileStorage._FileStorage__objects
            if key not in __objects:
                return
            fetched_obj = __objects[key]
            msg = f"attribute {attr_name} was not updated"
            self.assertTrue(hasattr(fetched_obj, attr_name), msg=msg)

            if hasattr(fetched_obj, attr_name):
                msg = f"'{attr_name}={attr_value}' was not updated"
                self.assertEqual(getattr(fetched_obj, attr_name), attr_value,
                                 msg=msg)

    def test_update_key_value(self):
        """check that key/value pair reflects in the __objects dict."""
        attr_name = 'xyz'
        attr_value = 'Test value'

        for _class in CLASSES:
            obj = eval(f"{_class}()")
            key = f"{_class}.{obj.id}"

            self.onecmd(f"update {_class} {obj.id} {attr_name} '{attr_value}'")

            __objects = FileStorage._FileStorage__objects
            if key not in __objects:
                return
            fetched_obj = __objects[key]
            msg = f"attribute {attr_name} was not updated"
            self.assertTrue(hasattr(fetched_obj, attr_name), msg=msg)

            if hasattr(fetched_obj, attr_name):
                msg = f"'{attr_name}={attr_value}' was not updated"
                self.assertEqual(getattr(fetched_obj, attr_name), attr_value,
                                 msg=msg)


@patch('sys.stdout', new_callable=StringIO)
class TestConsoleAllCommand(BaseCase):
    """Test all command."""

    @classmethod
    def setUpClass(cls):
        """Create objects for all classes."""
        super().setUpClass()
        cls.counts = {
            'BaseModel': 1,
            'User': 3,
            'State': 4,
            'City': 5,
            'Place': 10,
            'Amenity': 20,
            'Review': 50
        }
        cls.all_str_list = list()
        for _class, count in cls.counts.items():
            for i in range(count):
                obj = eval(f"{_class}()")
                cls.all_str_list.append(str(obj))

    def test_advanced_returns_list_look_alike(self, stdout):
        """check the advanced call <classname>.all()."""
        regex = r"^\[.*\]$"
        for _class in CLASSES:
            self.onecmd(f"{_class}.all()")
            msg = "all does not return a list look-alike"
            self.assertRegex(stdout.getvalue(), regex, msg=msg)
            stdout.seek(0)
            stdout.truncate(0)

    def test_returns_list_look_alike(self, stdout):
        """
        check that all returns a list lookalike
        """
        regex = r"^\[.*\]$"

        self.onecmd("all")
        msg = "all does not return a list look-alike"
        self.assertRegex(stdout.getvalue(), regex, msg=msg)

    def test_not_based_on_classname(self, stdout):
        """
        Check that all is called with no classname,
        Prints all string representation of all instances
        """
        self.onecmd("all")
        all_return = stdout.getvalue()

        for obj_str in self.__class__.all_str_list:
            self.assertIn(obj_str, all_return,
                          msg="certain obj_str not found in all return")

    def test_advanced_based_on_classname(self, stdout):
        """Checks <classname>.all()."""
        for _class in CLASSES:
            self.onecmd(f"{_class}.all()")
            all_return_list = eval(stdout.getvalue())
            actual_count = self.__class__.counts[_class]
            returned_count = len(all_return_list)

            msg = f'{_class}: expected {returned_count} got {actual_count}'
            self.assertEqual(actual_count, returned_count, msg=msg)

            stdout.seek(0)
            stdout.truncate(0)

    def test_based_on_classname(self, stdout):
        """
        Check that all <classname> prints only instance string representations
        of the objects of classname
        Principle:
        The number of elements in the returned list should compare with
            those in cls.counts dictionary
        """
        for _class in CLASSES:
            self.onecmd(f"all {_class}")
            all_return_list = eval(stdout.getvalue())
            actual_count = self.__class__.counts[_class]
            returned_count = len(all_return_list)

            msg = f'{_class}: expected {returned_count} got {actual_count}'
            self.assertEqual(actual_count, returned_count, msg=msg)

            stdout.seek(0)
            stdout.truncate(0)


class TestConsoleDestroyCommand(BaseCase):
    """Test destroy command."""

    def test_advanced_instance_deleted(self):
        """test <classname>.destroy(<id>)"""
        for _class in CLASSES:
            obj = eval(f"{_class}()")
            key = f"{_class}.{obj.id}"

            self.onecmd(f"{_class}.destroy({obj.id})")

            with open(test_path, 'r') as fp:
                dict_from_JSON = json.load(fp)

            msg = f"{_class} must not be in JSON file"
            self.assertNotIn(key, dict_from_JSON, msg=msg)

    def test_instance_deleted(self):
        """
        check that destroy actually removes an instance
        """
        for _class in CLASSES:
            obj = eval(f"{_class}()")
            key = f"{_class}.{obj.id}"

            self.onecmd(f"destroy {_class} {obj.id}")

            with open(test_path, 'r') as fp:
                dict_from_JSON = json.load(fp)

            self.assertNotIn(key, dict_from_JSON,
                             msg=f"{_class} must not be in JSON file")


@patch('sys.stdout', new_callable=StringIO)
class TestConsoleShowCommand(BaseCase):
    """Test show command."""

    def test_advanced_returns_str_representation(self, stdout):
        """Test <classname>.show(<id>)."""
        for _class in CLASSES:
            obj = eval(f"{_class}()")

            self.onecmd(f"{_class}.show({obj.id})")
            returned_str = stdout.getvalue().replace('\n', '')

            self.assertEqual(returned_str, str(obj))
            stdout.seek(0)
            stdout.truncate(0)

    def test_returns_str_representation(self, stdout):
        """
        check that show returns the __str__ representation of
        the object
        """
        for _class in CLASSES:
            obj = eval(f"{_class}()")

            self.onecmd(f"show {_class} {obj.id}")
            returned_str = stdout.getvalue().replace('\n', '')

            self.assertEqual(returned_str, str(obj))
            stdout.seek(0)
            stdout.truncate(0)


@patch('sys.stdout', new_callable=StringIO)
class TestConsoleCreateCommand(BaseCase):
    """Test create command."""

    def test_returns_id(self, stdout):
        """Check that id is returned for each class created."""
        for _class in CLASSES:
            self.onecmd(f"create {_class}")
            self.assertIsNotNone(stdout.getvalue())
            stdout.seek(0)
            stdout.truncate(0)

    def test_saved_to_JSON(self, stdout):
        """Check that created model is saved to JSON."""
        for _class in CLASSES:
            self.onecmd(f"create {_class}")
            _id = stdout.getvalue().replace('\n', '')

            key = f"{_class}.{_id}"
            with open(test_path, 'r') as fp:
                dict_from_JSON = json.load(fp)

            msg = f"created {_class} not saved in JSON file"
            self.assertIn(key, dict_from_JSON, msg=msg)
            stdout.seek(0)
            stdout.truncate(0)


@patch('sys.stdout', new_callable=StringIO)
class TestConsoleMissingErrors(BaseCase):
    """
    Test that errors are returned

    Attributes
    ----------
    no_attr : tuple
        error msg and list of methods that apply
    no_value : tuple
        error msg and list of methods that apply
    no_instance : tuple
        error msg and list of methods that apply
    noid : tuple
        error msg and list of methods that apply
    noclassname : tuple
        error msg and list of methods that apply
    noexist_classname : tuple
        error msg and list of methods that apply
    """

    no_attr = (
        "** attribute name missing **\n",
        ['update'])

    no_value = (
        "** value missing **\n",
        ['update'])

    no_instance = (
        "** no instance found **\n",
        ['show', 'destroy', 'update'])

    noid = (
        "** instance id missing **\n",
        ['show', 'destroy', 'update'])

    noclassname = (
        "** class name missing **\n",
        ['create', 'show', 'destroy', 'update'])

    noexist_classname = (
        "** class doesn't exist **\n",
        ['create', 'show', 'destroy', 'update', 'all'])

    def test_advanced_missing_attribute_name(self, stdout):
        """test advanced commands."""
        for _class in CLASSES:
            obj = eval(f"{_class}()")
            _id = obj.id

            self.onecmd(f"{_class}.update({_id})")
            self.assertEqual(TestConsoleMissingErrors.no_attr[0],
                             stdout.getvalue())
            stdout.seek(0)
            stdout.truncate(0)

    def test_missing_attribute_name(self, stdout):
        """
        check that when update is called with class and id but no attribute
        name, reports the error
        """
        for _class in CLASSES:
            obj = eval(f"{_class}()")
            _id = obj.id

            self.onecmd(f"update {_class} {_id} ")
            self.assertEqual(TestConsoleMissingErrors.no_attr[0],
                             stdout.getvalue())
            stdout.seek(0)
            stdout.truncate(0)

    def test_advanced_missing_value(self, stdout):
        """test advanced commands."""
        for _class in CLASSES:
            obj = eval(f"{_class}()")
            _id = obj.id

            self.onecmd(f"{_class}.update({_id}, name)")
            self.assertEqual(TestConsoleMissingErrors.no_value[0],
                             stdout.getvalue())
            stdout.seek(0)
            stdout.truncate(0)

    def test_missing_value(self, stdout):
        """
        check that when update is called with class, id and attribute name
        but no attribute value, reports the error
        """
        for _class in CLASSES:
            obj = eval(f"{_class}()")
            _id = obj.id

            self.onecmd(f"update {_class} {_id} name")
            self.assertEqual(TestConsoleMissingErrors.no_value[0],
                             stdout.getvalue())
            stdout.seek(0)
            stdout.truncate(0)

    def test_advanced_no_instance_found(self, stdout):
        """test advanced commands."""
        for command in TestConsoleMissingErrors.no_instance[1]:
            for _class in CLASSES:
                self.onecmd(f"{_class}.{command}(121212)")
                self.assertEqual(TestConsoleMissingErrors.no_instance[0],
                                 stdout.getvalue())
                stdout.seek(0)
                stdout.truncate(0)

    def test_no_instance_found(self, stdout):
        """
        check that each method when called with an id that does not exist,
        reports the error
        """
        for command in TestConsoleMissingErrors.no_instance[1]:
            for _class in CLASSES:
                self.onecmd(f"{command} {_class} 121212")
                self.assertEqual(TestConsoleMissingErrors.no_instance[0],
                                 stdout.getvalue())
                stdout.seek(0)
                stdout.truncate(0)

    def test_advanced_id_missing(self, stdout):
        """test advanced commands."""
        for command in TestConsoleMissingErrors.noid[1]:
            for _class in CLASSES:
                self.onecmd(f"{_class}.{command}()")
                self.assertEqual(TestConsoleMissingErrors.noid[0],
                                 stdout.getvalue())
                stdout.seek(0)
                stdout.truncate(0)

    def test_id_missing(self, stdout):
        """
        check that each method when called with each class but no id,
        reports the error
        """
        for command in TestConsoleMissingErrors.noid[1]:
            for _class in CLASSES:
                self.onecmd(f"{command} {_class}")
                self.assertEqual(TestConsoleMissingErrors.noid[0],
                                 stdout.getvalue())
                stdout.seek(0)
                stdout.truncate(0)

    def test_classname_missing(self, stdout):
        """
        check that each method when called with no class,
        reports the error
        """
        for command in TestConsoleMissingErrors.noclassname[1]:
            self.onecmd(f"{command} ")
            self.assertEqual(TestConsoleMissingErrors.noclassname[0],
                             stdout.getvalue())
            stdout.seek(0)
            stdout.truncate(0)

    def test_advanced_classname_no_exist(self, stdout):
        """test advanced tasks."""
        for command in TestConsoleMissingErrors.noexist_classname[1]:
            if command == 'create':
                continue
            self.onecmd(f"NonExistingClass.{command}()")
            self.assertEqual(TestConsoleMissingErrors.noexist_classname[0],
                             stdout.getvalue())
            stdout.seek(0)
            stdout.truncate(0)

    def test_classname_no_exist(self, stdout):
        """
        check that each method when called with a non existing class,
        reports an error
        """
        for command in TestConsoleMissingErrors.noexist_classname[1]:
            self.onecmd(f"{command} NonExistingClass")
            self.assertEqual(TestConsoleMissingErrors.noexist_classname[0],
                             stdout.getvalue())
            stdout.seek(0)
            stdout.truncate(0)
