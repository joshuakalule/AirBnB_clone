#!/usr/bin/python3
"""Contains the entry point of the command interpreter."""

import cmd
import shlex
from models import BaseModel, User, State, City, Amenity, Place, Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    Line-oriented command interpreter

    Attributes
    ----------
    prompt : str
        custorm prompt for the CLI
    """

    prompt = '(hbnb) '

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
            obj = _class
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
