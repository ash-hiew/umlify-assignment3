import unittest
from extractor import Extractor

"""Ten unit tests to test the extractor.py class, primarily the regex extractions"""


class ExtractorUnitTests(unittest.TestCase):
    """Tests for extractor.py`."""

    def test_class_extraction(self):
        """A class name can be extracted from line of code"""
        # Arrange
        e = Extractor().comp_ext
        expected = 'Marsupial'
        line = "class Marsupial(Mammal):"

        # Act
        actual = e._extract_class(line)

        # Assert
        self.assertEqual([expected], actual)

    def test_class_extraction_without_dependency(self):
        """A class name can be extracted from line of code where no parameters
         are set i.e. Python3 style"""
        e = Extractor().comp_ext
        # Arrange
        expected = 'Marsupial'
        line = "class Marsupial:"
        # Act
        actual = e._extract_class(line)
        # Assert
        self.assertEqual([expected], actual)

    def test_set_file(self):
        e = Extractor()
        expected = 7

        e.set_file(".\\tests")
        actual = len(e.get_component_dictionary())

        self.assertEqual(expected, actual)

    def test_set_file_file_not_found_error(self):
        e = Extractor()
        self.assertRaises(FileNotFoundError, e.set_file("test_class_unknown.py"))

    def test_nil_class_extraction(self):
        """A name will not be extracted from line of code where no class present"""
        # Arrange
        e = Extractor().comp_ext
        expected = []
        line = "class(Mammal):"

        # Act
        actual = e._extract_class(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_function_extraction(self):
        """A function name can be extracted from line of code"""
        # Arrange
        e = Extractor().comp_ext
        expected = 'proliferates'
        line = "def proliferates(self):"

        # Act
        actual = e. _extract_functions(line)

        # Assert
        self.assertEqual([expected], actual)

    def test_nil_function_extraction(self):
        """A name will not be extracted from line of code where no function present"""
        # Arrange
        e = Extractor().comp_ext
        expected = []
        line = "    teeth = 'Sharp'"

        # Act
        actual = e._extract_class(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_attribute_extraction(self):
        """An attribute name can be extracted from line of code"""
        # Arrange
        e = Extractor().comp_ext
        expected = 'teeth'
        line = "    self.teeth = 'Sharp'"

        # Act
        actual = e._extract_attributes(line)

        # Assert
        self.assertEqual([expected], actual)

    def test_nil_attribute_extraction(self):
        """A name will not be extracted from line of code where no attribute present"""
        # Arrange
        e = Extractor().comp_ext
        expected = []
        line = "    self.= 'Sharp'"

        # Act
        actual = e._extract_class(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_default_value_extraction(self):
        """An attribute default value can be extracted from line of code"""
        # Arrange
        e = Extractor().datatype_ext
        expected = 'Sharp'
        line = "    self.teeth = Sharp"

        # Act
        actual = e._extract_attribute_defaults(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_default_attribute_zero_length(self):
        # Arrange
        e = Extractor().datatype_ext
        expected = []
        line = "    self.teeth"

        # Act
        actual = e._extract_attribute_defaults(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_nil_default_value_extraction(self):
        """A value will not be extracted from line of code where no default present"""
        # Arrange
        e = Extractor().comp_ext
        expected = []
        line = "    self.teeth ='"

        # Act
        actual = e._extract_class(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_extraction(self):
        """An attribute data type can be extracted from line of code"""
        # Arrange
        e = Extractor().datatype_ext
        expected = 'str'
        line = "Sharp"

        # Act
        actual = e._extract_attribute_datatypes(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_object_extraction(self):
        e = Extractor().datatype_ext
        expected = 'obj'
        line = 'TEST()'

        # Act
        actual = e._extract_attribute_datatypes(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_dict_extraction(self):
        e = Extractor().datatype_ext
        expected = 'dict'
        line = '{test : 12}'

        # Act
        actual = e._extract_attribute_datatypes(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_list_extraction(self):
        e = Extractor().datatype_ext
        expected = 'list'
        line = '[12, 13, 14]'

        # Act
        actual = e._extract_attribute_datatypes(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_tuple_extraction(self):
        e = Extractor().datatype_ext
        expected = 'tuple'
        line = '("a", "b")'

        # Act
        actual = e._extract_attribute_datatypes(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_int_extraction(self):
        e = Extractor().datatype_ext
        expected = 'int'
        line = '5'

        # Act
        actual = e._extract_attribute_datatypes(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_str_extraction(self):
        e = Extractor().datatype_ext
        expected = 'str'
        line = "'test'"

        # Act
        actual = e._extract_attribute_datatypes(line)

        # Assert
        self.assertEqual(expected, actual)

    def test_unknown_data_type_extraction(self):
        """An error message is raised when an unknown attribute data type is extracted from line of code"""
        # Arrange
        e = Extractor().datatype_ext

        line = '@'

        # Act

        # Assert
        with self.assertRaises(ValueError) as context:
            e._extract_attribute_datatypes(line)
        self.assertTrue("No data type detected for '@'" in str(context.exception))

    def test_non_attribute_extraction(self):
        """Handles data in __init__ that have are not attributes"""
        e = Extractor().datatype_ext
        # Arrange
        expected = []
        line = '  self.setup()'
        # Act
        actual = e._extract_attribute_defaults(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_string_extraction(self):
        """An attribute data type can be extracted from line of code"""
        e = Extractor().datatype_ext
        # Arrange
        expected = 'str'
        line = "Sharp"
        # Act
        actual = e._extract_attribute_datatypes(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_string_variation_extraction(self):
        """An attribute data type can be extracted from line of code"""
        e = Extractor().datatype_ext
        # Arrange
        expected = 'str'
        line = "'"
        # Act
        actual = e._extract_attribute_datatypes(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_data_type_dictionary_extraction(self):
        """An attribute data type can be extracted from line of code"""
        e = Extractor().datatype_ext
        # Arrange
        expected = 'dict'
        line = "{"
        # Act
        actual = e._extract_attribute_datatypes(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_attribute_declared(self):
        e = Extractor()
        # Arrange
        expected = True
        # Act
        e._data_extraction("./component.py")
        if e.component_dict:
            actual = True
        else:
            actual = False
        # Assert
        self.assertEqual(actual, expected)

    def test_single_dependency_extraction(self):
        """Extracts a single object that class inherits from"""
        e = Extractor().comp_ext
        # Arrange
        expected = ["Test1"]
        line = 'class Example(Test1)'
        # Act
        actual = e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_extract_parents_without_parent(self):
        e = Extractor().comp_ext
        expected = ""
        line = 'Example(Test1)'
        # Act
        actual = e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_object_only_dependency_(self):
        """Does not extract 'object' if it is only dependency"""
        e = Extractor().comp_ext
        # Arrange
        expected = []
        line = 'class Example(object)'
        # Act
        actual = e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_multiple_dependency_extraction(self):
        e = Extractor().comp_ext
        # Arrange
        expected = ["Test1", "Test2", "Test3"]
        line = 'class Example(Test1, Test2, Test3)'
        # Act
        actual = e._extract_parents(line)
        # Assert
        self.assertEqual(expected, actual)

    def test_class_name(self):
        e = Extractor()
        expected = True
        e._data_extraction("./mammals.py")
        if e.component_dict:
            actual = True
        else:
            actual = False
        self.assertEqual(actual, expected)

    def test_extractor_class_get_function(self):
        """Ensure that getter can retrieve a dictionary"""
        e = Extractor()
        e._data_extraction("./tests/test_class_5.py")
        dictionary = e.get_component_dictionary()
        self.assertTrue(dictionary)


if __name__ == '__main__':
    unittest.main(verbosity=2)
