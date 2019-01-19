from unittest import main, TestCase, mock
from database import Database
from shelf import Shelf
from interpreter import Interpreter
from controller import InterpreterController
from os import path
from shutil import rmtree
import io


class InterpreterTests(TestCase):

    def setUp(self):
        database = Database()
        shelf = Shelf()
        self.interp = Interpreter()
        self.cont = InterpreterController(self.interp, database, shelf)
        self.interp.attach(self.cont)
        if path.exists("output"):
            rmtree("output")

    def test_do_file(self):
        # Arrange
        test_file = './tests/test_class_5.py'
        # Act
        self.interp.do_file(test_file)
        # Assert
        self.assertEqual(self.cont.input_path, test_file)

    def test_do_directory(self):
        # Arrange
        test_file = './tests/test_class_5.py'
        # Act
        self.interp.do_directory(test_file)
        # Assert
        self.assertEqual(self.cont.input_path, test_file)

    def do_location(self):
        # Arrange
        test_file = 'output/'
        # Act
        self.interp.do_location(test_file)
        # Assert
        self.assertEqual(self.cont.output_path, test_file)

    def test_do_type(self):
        # Arrange
        file_type = 'png'
        # Act
        self.interp.do_type(file_type)
        # Assert
        self.assertEqual(self.cont.output_file_type, file_type)

    def test_do_run(self):
        # Arrange
        test_file = './tests/test_class_5.py'
        self.interp.do_file(test_file)
        # Act
        self.interp.do_run("")
        # Assert
        self.assertTrue(self.cont.run)

    def test_check_run(self):
        # Arrange
        test_file = './tests/test_class_5.py'
        self.interp.do_file(test_file)
        self.interp.do_run("")
        # Act
        result = self.cont._check_run()
        # Assert
        self.assertTrue(result)

    def test_check_input(self):
        # Arrange
        test_file = './tests/test_class_5.py'
        self.interp.do_file(test_file)
        # Act
        result = self.cont._check_input()
        # Assert
        self.assertTrue(result)

    def test_do_bar_chart(self):
        # Arrange
        test_file = './tests/test_class_5.py'
        test_output_file = 'bar-chart'
        fname = "output/bar-chart.png"
        self.interp.do_file(test_file)
        self.interp.do_run("")
        # Act
        self.interp.do_bar_chart(test_output_file)
        # Assert
        self.assertTrue(path.isfile(fname))

    def test_do_pie_chart(self):
        # Arrange
        test_file = './tests/test_class_5.py'
        fname = "output/Plant-pie-chart.png"
        self.interp.do_file(test_file)
        self.interp.do_run("")
        # Act
        self.interp.do_pie_chart()
        # Assert
        self.assertTrue(path.isfile(fname))

    def test_execute_if_location(self):
        # Arrange
        self.cont.command = "location"
        expected = "output/"

        # Act
        self.cont.execute()
        self.cont.set_location("output/")
        actual = self.cont.output_path

        # Assert
        self.assertEqual(expected, actual)

    def test_execute_if_database(self):
        # Arrange
        self.cont.command = "database"
        expected = "Please select an input path with \"file\" or \"directory\"\n"

        # Act
        self.cont.execute()
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cont.use_database("")

        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())

    def test_execute_if_shelf(self):
        # Arrange
        self.cont.command = "shelf"
        expected = "Please select an input path with \"file\" or \"directory\"\n"

        # Act
        self.cont.execute()
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cont.use_shelf("")

        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())

    def test_set_file_without_input(self):
        # Arrange
        expected = "Please enter a file to use as input\n"

        # Act
        self.cont.execute()
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cont.set_file(None)

        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())

    def test_run_umlify_without_input_path(self):
        # Arrange
        expected = "Please select an input path with \"file\" or \"directory\"\n"
        self.cont.input_path = None

        # Act
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cont.run_umlify()

        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())

    def test_set_directory_without_input(self):        # Arrange
        expected = "Please enter a directory to use as input\n"

        # Act
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.cont.set_directory(None)

        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())


if __name__ == '__main__':
    main(verbosity=2)
