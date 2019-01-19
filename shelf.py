import shelve
import os
from extractor import Extractor
import dbm

"""This module consists of functions that serializes and de-serializes 
    the data of Component objects and storing them into a database known as a shelf. 
    The shelf is accessed by using keys, just like a dictionary. 
    The shelve module provides object persistence and object serialization by using the pickle module.
"""


class Shelf(object):
    def __init__(self):
        self.shelf_name = None

    def set_shelf(self, shelf_input):
        self.shelf_name = shelf_input

    def write_shelf(self, selected_file):
        """Add component data dictionary to shelf file"""

        dict_item = self.extract_data(selected_file)
        key = os.path.basename(selected_file).strip('.py')

        if dict_item != {}:
            with shelve.open(self.shelf_name, "c") as shelf:
                try:
                    shelf[key] = dict_item
                    str_format = "Class components of [{}] serialized and stored to file successfully"
                    print(str_format.format(key))
                except (KeyError, ValueError):
                    raise("Duplicate Error: File is already stored in shelf {}".format(self.shelf_name))
        else:
            print("[{}] cannot be stored to shelf. File does not exist.".format(selected_file))

    @staticmethod
    def extract_data(file):
        """"Uses extraction method from Extractor class"""
        ext = Extractor()
        ext.set_file(file)
        return ext.get_component_dictionary()

    def read_selected_from_shelf(self, selected_file):
        """Read selected component data from shelf file"""

        with shelve.open(self.shelf_name, 'r') as shelf:
            try:
                dict_item = shelf[selected_file]
            except KeyError:
                raise Exception("Selected key name cannot be found in shelf [{}]".format(self.shelf_name))

        output = self._display_components(dict_item)

        return output

    def read_shelf(self):
        """Read component data from shelf file"""
        shelf_dict = {}

        output = ""
        with shelve.open(self.shelf_name, 'r') as shelf:
            for key in shelf.keys():
                item = shelf[key]
                shelf_dict[key] = item

        for key, dict_item in shelf_dict.items():
            output += "KEY: " + key.upper() + "\n"
            output += self._display_components(dict_item)
        return output

    def delete_key_from_shelf(self, key_input):
        with shelve.open(self.shelf_name) as shelf:
                del shelf[key_input]

    @staticmethod
    def _display_components(dict_item):
        new_line = "\n"
        output = ""

        for class_name, class_data in dict_item.items():
            output += "Class Name: " + class_data.name + new_line
            for attr in class_data.attributes:
                output += "Attribute: " + attr + new_line
            for func in class_data.functions:
                output += "Function: " + func + new_line
            for parent in class_data.parents:
                output += "Parent: " + parent.name + new_line
            output += "-" * 20 + new_line
        return output

    def clear_shelf(self):
        """Removes all Component objects stored within the file"""
        with shelve.open(self.shelf_name) as shelf:
                shelf.clear()

