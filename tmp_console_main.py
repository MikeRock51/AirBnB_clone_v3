#!/usr/bin/python3
"""Entry point of the command interpreter"""


import cmd
import json
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class_list = {
    'BaseModel': BaseModel,
    'User': User,
    'Place': Place,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Review': Review
}


class HBNBCommand(cmd.Cmd):
    """Implementation of the console's commands"""

    prompt = '(hbnb) '

    def do_quit(self, line):
        """Exits the interpreter"""
        print("You say make I QUIT?")
        return True

    do_EOF = do_quit

    def emptyline(self):
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel"""
        line = line.split()
        if not line:
            print('** class name missing **')
        elif line[0] not in class_list:
            print("** class doesn't exist **")
        else:
            if len(line) == 1:
                instance = class_list[line[0]]()
            else:
                kwargs = {}
                for param in line[1:]:
                    params = param.split('=')
                    key = params[0]
                    value = eval(params[1].replace('_', ' '))
                    kwargs[key] = value
                instance = class_list[line[0]](**kwargs)
            instance.save()
            print(instance.id)

    def do_show(self, line):
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in class_list:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            try:
                instance = storage.all()["{}.{}".format(args[0], args[1])]
                print(instance)
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in class_list:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            try:
                del (storage.all()["{}.{}".format(args[0], args[1])])
                storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, line):
        """Prints all string representation of all instances"""
        all_instances = storage.all()
        class_instances = []

        if line and line not in class_list:
            print("** class doesn't exist **")
            return False
        else:
            for instance in all_instances.values():
                if line:
                    if instance.__class__.__name__ == line:
                        class_instances.append(str(instance))
                else:
                    class_instances.append(str(instance))
        print(class_instances)

    def do_update(self, line):
        """Updates an instance based on class name and id"""
        args = line.split()
        args = args[:4]
        # [class_name, id, attr_name, attr_value] =\
        # [arg for arg in args]
        if not line:
            print("** class name missing **")
            return False
        elif args[0] not in class_list:
            print("** class doesn't exist **")
            return False
        elif len(args) < 2:
            print("** instance id missing **")
            return False
        elif len(args) < 3:
            print("** attribute name missing **")
            return False
        elif len(args) < 4:
            print("** value missing **")
            return False
        else:
            try:
                instance = storage.all()["{}.{}".format(args[0], args[1])]
            except KeyError:
                print("** no instance found **")
                return False
            setattr(instance, args[2], eval(args[3]))
            instance.save()

    def do_count(self, line):
        """Retrieves the number of instances of a class"""
        if not line:
            print("** class name missing **")
        elif line not in class_list:
            print("** class doesn't exist **")
        else:
            count = 0
            all_instances = storage.all()
            for instance in all_instances.values():
                if instance.__class__.__name__ == line:
                    count += 1
            print(count)

    def help_show(self):
        print('\n'.join(["Prints the string representation of an instance",
                         "based on class name and id"]))

    def parseline(self, line):
        """Parses commands to suit console syntax before execution"""
        if '.' in line and '=' not in line:
            parsed_line = line.split('.')
            if '"' in parsed_line[1]:
                if parsed_line[1].split('(')[0] == 'update':
                    if '{' in parsed_line[1].split(',')[1]:
                        id = parsed_line[1].split('"')[1]
                        kwargs = parsed_line[1].split(',', 1)[1].strip(' )')
                        kwargs = kwargs.replace("'", '"')
                        kwargs = json.loads(kwargs)
                        for i, (key, value) in enumerate(kwargs.items()):
                            if i < len(kwargs) - 1:
                                self.onecmd("update {} {} {}'{}'".format(
                                    parsed_line[0], id, key, value))
                            else:
                                parsed_line = (
                                    "update", parsed_line[0], id, key,
                                    str(value))
                    else:
                        clean_line = [ln for ln in parsed_line[1].split(
                            '"')[1:] if ln != ", " and ln != ')']
                        id = clean_line[0]
                        attr_name = clean_line[1]
                        attr_value = "'{}'".format(clean_line[2])
                        parsed_line = ("update", parsed_line[0], id,
                                       attr_name, attr_value)
                else:
                    id = parsed_line[1].split('"')[1]
                    parsed_line = parsed_line[1].split('(')[0], parsed_line[0]
                    parsed_line = parsed_line + (id,)
            else:
                parsed_line = parsed_line[1].strip('()'), parsed_line[0]
            parsed_line = ' '.join(parsed_line)
            return cmd.Cmd.parseline(self, parsed_line)
        else:
            return cmd.Cmd.parseline(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
