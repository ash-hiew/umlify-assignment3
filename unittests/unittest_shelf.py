from unittest import TestCase, main
from shelf import Shelf
import shelve
import os


class ShelfUnitTests(TestCase):
    """Unittests for Shelf"""
    def setUp(self):
        self.shelf = Shelf()
        self.shelf.shelf_name = "test_shelve"

    def tearDown(self):
        if os.path.exists("test_shelve.dat"):
            os.remove('test_shelve.dat')
            os.remove('test_shelve.bak')
            os.remove('test_shelve.dir')

    def test_write_shelf(self):
        # Act
        self.shelf.write_shelf("tests/test_class_2.py")
        with shelve.open(self.shelf.shelf_name) as shelf:
            actual = bool(shelf)

        # Assert
        self.assertTrue(actual)

    def test_write_shelf_if_shelf_name_none(self):
        # Act
        actual = self.shelf.write_shelf("tests/test_class_2.py")

        # Assert
        self.assertIsNone(actual)

    def test_read_shelf(self):
        # Arrange
        self.shelf.write_shelf("tests/test_class_5.py")
        expected = "KEY: TEST_CLASS_5\n"
        expected += "Class Name: Plant\n"
        expected += "Attribute: plant_height\n"
        expected += "Function: __init__\n"
        expected += "Function: grow_plant\n"
        expected += "-"*20 + "\n"
        expected += "Class Name: Sunflower\n"
        expected += "Function: drop_seed\n"
        expected += "Parent: Plant\n"
        expected += "-"*20 + "\n"
        expected += "Class Name: Orchid\n"
        expected += "Parent: Plant\n"
        expected += "-"*20 + "\n"

        # Act
        actual = self.shelf.read_shelf()

        # Assert
        self.assertMultiLineEqual(expected, actual)

    def test_read_shelf_two_dict(self):
        self.shelf.write_shelf("./tests/test_class_1.py")
        self.shelf.write_shelf("tests/test_class_5.py")

        expected = "KEY: TEST_CLASS_1\n"
        expected += "Class Name: DemoClass\n"
        expected += "-" * 20 + "\n"
        expected += "KEY: TEST_CLASS_5\n"
        expected += "Class Name: Plant\n"
        expected += "Attribute: plant_height\n"
        expected += "Function: __init__\n"
        expected += "Function: grow_plant\n"
        expected += "-" * 20 + "\n"
        expected += "Class Name: Sunflower\n"
        expected += "Function: drop_seed\n"
        expected += "Parent: Plant\n"
        expected += "-" * 20 + "\n"
        expected += "Class Name: Orchid\n"
        expected += "Parent: Plant\n"
        expected += "-" * 20 + "\n"

        # Act
        actual = self.shelf.read_shelf()

        # Assert
        self.assertEqual(expected, actual)

    def test_read_shelf_exception_thrown(self):
        self.shelf.shelf_name = None
        with self.assertRaises(Exception):
            self.shelf.read_shelf()

    def test_clear_shelf(self):
        # Arrange
        self.shelf.clear_shelf()
        expected = []

        # Act
        with shelve.open(self.shelf.shelf_name, 'r') as test_file:
            actual = list(test_file.keys())

        # Assert
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    main(verbosity=2)
