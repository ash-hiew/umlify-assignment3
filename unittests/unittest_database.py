import unittest
from database import Database
import sqlite3 as sql
import os
from unittest import mock, TestCase, main
import io


class DatabaseUnitTests(TestCase):
    """Unittests for Database"""
    def setUp(self):
        self.db = Database()
        self.filename = "unittests/test_case.db"
        self.db.db_name = "test_case.db"

    def tearDown(self):
        if self.db._conn is not None:
            self.db.drop_table()
        if os.path.exists('unittests/test_case.db'):
            os.remove('unittests/test_case.db')
        if os.path.exists('unittests/test.db'):
            os.remove('unittests/test.db')

    def test_database_created(self):
        # Arrange
        self.db.create_connection(self.filename)
        self.db.drop_table()
        self.db.create_table()

        # Act
        actual = os.path.isfile("unittests/test_case.db")

        # Assert
        self.assertTrue(actual)

    def test_create_connection_called_exception(self):
        with self.assertRaises(sql.Error):
            self.db.create_connection(None)

    def test_if_directory_path(self):
        self.db.create_connection(self.filename)
        expected = "unittests/"

        actual = self.db.file_path

        self.assertEqual(expected, actual)

    def test_if_not_directory_path(self):
        self.filename = "test.db"
        self.db.create_connection(self.filename)
        expected = ""

        actual = self.db.file_path

        self.assertEqual(expected, actual)

    def test_query_exception_thrown(self):
        self.db.file_path = None
        self.db.db_name = None
        expected = "Please connect to a database first\n"

        # Act
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.db.query("DROP TABLE IF EXISTS classes")

        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())

    def test_extract_data(self):
        filename = "./tests/test_class_2.py"

        actual = self.db.extract_data(filename)

        self.assertIsInstance(actual, dict)

    def test_close_connection(self):
        # Arrange
        self.db.create_connection(self.filename)

        # Assert
        self.assertIsNone(self.db.close_connection())

    def test_table_created(self):
        # Arrange
        self.db.create_connection(self.filename)
        self.db.drop_table()
        self.db.create_table()

        # Act
        statement = "SELECT name FROM sqlite_master WHERE type='table'"
        self.db.query(statement)
        result = bool(self.db._cursor.fetchone())

        self.db._conn.close()

        # Assert
        self.assertTrue(result)

    def test_add_to_database(self):
        # Arrange
        self.db.create_connection(self.filename)
        expected = "Class Name:Person\n"
        expected += "Attribute:{'name': {'str': 'new_name'}, 'age': {'str': 'new_age'}}\n"
        expected += "Function:['__init__']\n"
        expected += "-" * 20 + "\n"

        # Act
        self.db.insert_data('./tests/test_class_2.py')
        actual = self.db.get_specific('./tests/test_class_2.py')

        # Assert
        self.assertEqual(expected, actual)

    def test_duplicate_data_exception_thrown(self):
        self.db.file_path = "./tests/"
        self.db.db_name = "test_case.db"
        test_file = "./tests/test_class_2.py"
        self.db.create_table()
        expected = 'Duplication Error: file has already been added\n'

        self.db.insert_data(test_file)

        # Act
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.db.insert_data(test_file)

        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())

    def test_insert_data_cannot_add(self):
        # Arrange
        self.db.db_name = "test_case.db"
        test_file = "./tests/test_class_0.py"
        expected = 'Error: File not found\n'
        expected += 'Cannot add test_class_0 to database\n'
        self.db.create_table()

        # Act
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.db.insert_data(test_file)

        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())

    def test_get_db_info(self):
        # Arrange
        self.db.create_connection(self.filename)
        expected = "Selected Database: test_case.db" + "\n"
        expected += "The number of pickled files in the database: 0"

        # Act
        actual = self.db.get_db_info()

        # Assert
        self.assertEqual(expected, actual)

    def test_get_db_info_close_conn(self):
        self.db.create_connection(self.filename)

        self.db.get_db_info()

        self.assertTrue(self.db._conn.close)

    def test_remove_data(self):
        self.db.create_connection(self.filename)
        expected = 1

        self.db.insert_data("tests/test_class_2.py")
        self.db.insert_data("tests/test_class_3.py")
        self.db.remove_data("tests/test_class_3.py")

        self.db._conn = sql.connect(self.filename)
        self.db._cursor = self.db._conn.cursor()
        self.db._cursor.execute("SELECT COUNT(*) FROM classes")
        actual = self.db._cursor.fetchone()[0]

        self.assertEqual(expected, actual)

    @unittest.skip("This is meant for validator")
    def test_remove_data_invalid(self):
        # Arrange
        self.db.create_connection(self.filename)
        self.db.db_name = "test_case.db"
        test_file = "./tests/test_class_1.py"
        self.db.insert_data("./tests/test_class_2.py")
        self.db.insert_data("./tests/test_class_3.py")

        expected = 'Cannot remove test_class_1.py from database\n'

        # Act
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.db.remove_data(test_file)

        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())

    def test_get_specific(self):
        # Arrange
        self.db.create_connection(self.filename)
        expected = "Class Name:DemoClass\n"
        expected += "Attribute:[]\n"
        expected += "Function:[]\n"
        expected += "-" * 20 + "\n"

        # Act
        self.db.insert_data('./tests/test_class_1.py')
        actual = self.db.get_specific('./tests/test_class_1.py')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_specific_filename_stripped_of_py(self):
        # Arrange
        self.db.create_connection(self.filename)
        expected = "Class Name:DemoClass\n"
        expected += "Attribute:[]\n"
        expected += "Function:[]\n"
        expected += "-" * 20 + "\n"

        # Act
        self.db.insert_data('./tests/test_class_1.py')
        actual = self.db.get_specific('test_class_1')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_specific_sql_exception_thrown(self):
        self.db.create_connection(self.filename)
        with self.assertRaises(Exception):
            self.db.get_specific(None)

    def test_get_all(self):
        # Arrange
        self.db.create_connection(self.filename)
        expected = "Class Name:Plant\n"
        expected += "Attribute:{'plant_height': {'str': 'h'}}\n"
        expected += "Function:['__init__', 'grow_plant']\n"
        expected += "-" * 20 + "\n"
        expected += "Class Name:Sunflower\n"
        expected += "Attribute:[]\n"
        expected += "Function:['drop_seed']\n"
        expected += "Parent:Plant\n"
        expected += "-" * 20 + "\n"
        expected += "Class Name:Orchid\n"
        expected += "Attribute:[]\n"
        expected += "Function:[]\n"
        expected += "Parent:Plant\n"
        expected += "-" * 20 + "\n"
        expected += "Class Name:Person\n"
        expected += "Attribute:{'name': {'str': 'new_name'}, 'age': {'str': 'new_age'}}\n"
        expected += "Function:['__init__']\n"
        expected += "-" * 20 + "\n"
        expected += "The number of components in the database: 4"

        # Act
        self.db.insert_data('./tests/test_class_5.py')
        self.db.insert_data('./tests/test_class_2.py')
        actual = self.db.get_all()

        # Assert
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    main(verbosity=2)
