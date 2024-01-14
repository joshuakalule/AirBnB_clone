#!/usr/bin/python3
"""Contains the entry point of the command interpreter."""

import cmd
import shlex
import re
import json
from models import BaseModel, User, State, City, Amenity, Place, Review
from models import storage


METHODS_CMD = ["all", "show", "destroy", "update", "count"]


class HBNBCommand(cmd.Cmd):
    """
    Line-oriented command interpreter

    Attributes
    ----------
    prompt : str
        custorm prompt for the CLI
    """

    prompt = '(hbnb) '

    def update_dict(self, class_name, obj_id, dict_str):
        """
        Update an instance based on the class name and id using
        a dictionary representation Save the change into the JSON file
        """
        obj_id = obj_id.strip('"')
        key, instance = retrieve(class_name, obj_id)
        if not key:
            print(obj_id)
            return
        try:
            dict_str = str(dict_str)
            dict_str = dict_str.replace("'", "\"")
            attr_dict = json.loads(dict_str)
        except json.JSONDecodeError:
            print("** invalid dictionary **")
            return

        for attr_name, attr_value in attr_dict.items():
            if hasattr(instance, attr_name):
                attr_type = type(getattr(instance, attr_name))
                setattr(instance, attr_name, attr_type(attr_value))
            else:
                setattr(instance, attr_name, attr_value)
        instance.save()

    def count(self, class_name):
        """
        retrieve the number of instances of a class
        """
        count_obj = 0
        for key in storage.all():
            if key.startswith(class_name):
                count_obj += 1
        print(count_obj)

    def default(self, line):
        """
        Process unknown commands by finding pattern
        in available methods and passing them on to reconstruction
        method
        """
        # <class_name>.<method>(<args>)
        regex_txt = r"(\w+)\.(\w+)\((.*)\)"
        # <class name>.update(<id>, <dictionary representation>)
        pattern = r"\(([^)]+),\s*({.*})\)"
        match = re.match(regex_txt, line)

        if not match:
            return super().default(line)

        class_name = match.group(1)
        method_name = match.group(2)
        # search for id and dictionary representation
        update_args = re.search(pattern, line)
        args = match.group(3).split(',') if match.group(3) else []

        if method_name not in METHODS_CMD:
            return super().default(line)

        if method_name == "count":
            self.count(class_name)
        elif method_name == "update":
            if update_args:
                obj_id = update_args.group(1)
                dict_str = update_args.group(2)
                self.update_dict(class_name, obj_id, dict_str)
            else:
                self.re_arrange(class_name, method_name, args)
        else:
            self.re_arrange(class_name, method_name, args)

    def re_arrange(self, class_name, method_name, args):
        """
        Re-construct command to fit in with command line interpreter
        """
        args_str = " ".join(args)
        if len(args_str) == 0:
            command = f"{method_name} {class_name}"
        else:
            command = f"{method_name} {class_name} {args_str}"
        self.execute_command(command)

    def execute_command(self, command):
        """
        Execute reconstructed command to the appropriate method
        """
        return self.onecmd(command)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute
        Save the change into the JSON file
        """
        args = parse(arg)
        key, instance = retrieve(*args)

        if not key:
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        attr_name = args[2]
        attr_value = args[3]

        if hasattr(instance, attr_name):
            attr_type = type(getattr(instance, attr_name))
            setattr(instance, attr_name, attr_type(attr_value))
        else:
            setattr(instance, attr_name, attr_value)
        instance.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not on
        the class name
        """
        args = parse(arg)
        criterion = None

        if args:
            """Set print criterion based on class name."""
            classname = args[0]
            if class_exists(classname):
                criterion = classname
            else:
                return

        return_list = list()
        for key, obj in storage.all().items():
            if criterion:
                if key.startswith(criterion):
                    return_list.append(str(obj))
            else:
                return_list.append(str(obj))
        print(return_list)

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        Changes saved into the JSON file
        """
        args = parse(arg)
        key, instance = retrieve(*args)
        if key in storage.all():
            del storage.all()[key]
            storage.save()

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the class
        name and id.
        """
        args = parse(arg)
        key, instance = retrieve(*args)
        if instance:
            print(instance)

    def do_create(self, classname):
        """
        Creates a new instance of classname, saves it (to the JSON file)
        and prints the id.
        """
        if (_class := class_exists(classname)):
            obj = _class()
            obj.save()
            print(obj.id)

    def do_EOF(self, line):
        """Cleanly exit the program."""
        print()
        return True

    def do_quit(self, line):
        """Exits the program."""
        return True

    def emptyline(self):
        """Idles when Empty line + ENTER."""
        pass


def class_exists(class_to_check, type_to_check=BaseModel):
    """
    Check whether the class_to_check exists and is a subclass of
    type_to_check
    Returns the class
    """
    if not class_to_check:
        print("** class name missing **")
        return None

    _class = globals().get(class_to_check)
    if class_to_check in globals() and issubclass(_class, type_to_check):
        return _class
    else:
        print("** class doesn't exist **")
        return None


def retrieve(classname=None, obj_id=None, *args):
    """
    check if the classname and instance with obj_id exists
    returns the key-obj_instance pair
    """

    if not class_exists(classname):
        return None, None

    if not obj_id:
        print("** instance id missing **")
        return None, None

    key = f"{classname}.{obj_id}"
    if not (obj := storage.all().get(key)):
        print("** no instance found **")
        return None, None

    return (key, obj)


def parse(line):
    """
    Convert a series of zero or more strings to an argument tuple
    method shlex.split() avoids splitting argument parts enclosed in quotes
    """
    return tuple(shlex.split(line))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
