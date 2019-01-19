from component import Component
from component_extractor import ComponentExtractor
from datatype_extractor import DataTypeExtractor
import os
import glob

""" This module receives data from files or folders then
 extracts class names, dependencies, function names and attribute details.
 For each class it creates a new Component object and places the above details in that object.
 This module then outputs a dictionary containing the Component objects for that file/folder    
"""


class Extractor(object):

    def __init__(self):
        self.file = ''
        self.component_dict = {}
        self.attribute_dict = {}
        self.comp = None
        self.comp_ext = ComponentExtractor()
        self.datatype_ext = DataTypeExtractor()

    def set_file(self, file_path):
        try:
            file_string = file_path
            if os.path.isfile(file_string):
                self._data_extraction(file_string)
            elif os.path.isdir(file_string):
                files = glob.glob(file_string + '/**/*.py', recursive=True)
                for item in files:
                    print('Item = %s' % item)
                    self._data_extraction(item)
            else:
                print("Error: File not found")
        except FileNotFoundError:  # pragma: no cover
            print('This file cannot be found')

    def _data_extraction(self, file_path):
        with open(file_path, 'r') as sourcefile:
            for line in sourcefile:
                class_name = self.comp_ext._extract_class(line)
                function_name = self.comp_ext._extract_functions(line)
                attribute_name = self.comp_ext._extract_attributes(line)
                if class_name:
                    self.add_class_and_parent_to_dict(class_name, line)
                elif function_name:
                    self.add_function_to_dict(function_name)
                elif attribute_name:
                    self.add_attribute_to_dict(attribute_name, line)

    def add_class_and_parent_to_dict(self, class_name, line):
        self.comp = self.component_dict.get(class_name[0])
        if self.comp is None:
            self.comp = Component()
        self.comp.set_name(class_name[0])
        parent = self.comp_ext._extract_parents(line)
        for item in parent:
            if item != 'object':  # pragma: no cover
                parent = self.component_dict.get(item)
                if parent is None:
                    parent = Component()
            self.comp.get_parents().append(parent)
        self.component_dict[class_name[0]] = self.comp

    def add_function_to_dict(self, function_name):
        try:
            function_name = function_name[0]
            self.comp.get_functions().append(function_name)
        except UnboundLocalError as err:  # pragma: no cover
            print('Class has not been declared for "{0}" function'.format(function_name))
            print(err)
            return

    def add_attribute_to_dict(self, attribute_name, line):
        attr_name = None
        try:
            if self.comp.get_functions() == ['__init__']:
                attr_name = attribute_name[0]
                data_type_dict = self.datatype_ext._extract_defaults_datatypes(line)
                self.attribute_dict[attr_name] = data_type_dict
                self.comp.set_attributes(self.attribute_dict)
        except UnboundLocalError as err:  # pragma: no cover
            print('Class has not been declared for "{0}" attribute'.format(attr_name))
            print(err)
            return

    def get_component_dictionary(self):
        return self.component_dict

