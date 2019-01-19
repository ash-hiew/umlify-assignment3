"""
Defines application behaviour.
This is the controller part of the MVC architecture.
Maps user actions to Model updates
"""

from os import path
from abc import ABCMeta, abstractmethod
from visual_generator import VisualGenerator


class Observer(metaclass=ABCMeta):
    def __init__(self):
        self.command = None
        self.input = None

    @abstractmethod
    def update(self):   # pragma: no cover
        pass


class InterpreterController(Observer):
    """
    Controller class that interacts with the model (Interpreter)
    """
    def __init__(self, interpreter, db, shelf):
        Observer.__init__(self)
        self.subject = interpreter
        self.db = db
        self.vg = None
        self.shelf = shelf
        self.input_path = None
        self.output_path = None
        self.run = False
        self.allowed_types = ["dot", "png", "pdf"]
        self.directory = path.realpath(path.curdir)
        # default output file type .dot (first in allowed types)
        self.output_file_type = self.allowed_types[0]

    def start(self):    # pragma: no cover
        self.subject.cmdloop()

    def get_command(self):
        return self.subject.get_command()

    def get_input(self):
        return self.subject.get_input()

    def update(self):
        self.command = self.get_command()
        self.input = self.get_input()
        self.execute()

    def execute(self):
        if self.command == "file":
            self.set_file(self.input)
        elif self.command == "type":
            self.set_type(self.input)
        elif self.command == "run":
            self.run_umlify()
        elif self.command == "directory":
            self.set_directory(self.input)
        elif self.command == "location":
            self.set_location(self.input)
        elif self.command == "database":
            self.use_database(self.input)
        elif self.command == "shelf":
            self.use_shelf(self.input)
        elif self.command == "pie_chart":
            self.make_pie_chart(self.input)
        elif self.command == "bar_chart":
            self.make_bar_chart(self.input)

    def set_file(self, file):
        if file:
            self.input_path = file
            print("Input file set to \"{file}\"".format(file=file))
        else:
            print("Please enter a file to use as input")

    def set_type(self, file_type):  # pragma: no cover
        if not file_type:
            # no file type was provided
            print("Please enter a file type")
            return

        file_type = file_type.lower()  # convert to all lowercase

        # remove leading . if given (eg .png instead of png)
        if file_type[0] == ".":
            file_type = file_type[1:]

        if file_type == self.output_file_type:
            print("The output file type is already {file_type}".format(file_type=file_type))
        elif file_type in self.allowed_types:
            self.output_file_type = file_type
            print("Output file type has been set to {file_type}".format(file_type=file_type))
        else:
            # input provided was not in the list of allowed types
            print("That file type is not supported, please pick one from: {file_types}".format(
                file_types=', '.join(self.allowed_types)))

    def run_umlify(self):
        if not self.input_path:
            print("Please select an input path with \"file\" or \"directory\"")
            return
        self.vg = VisualGenerator(self.input_path, self.output_path)
        self.vg.generate_diagram()
        self.run = True
        print("Running Umlify...")

    def set_directory(self, directory):
        if directory:
            self.input_path = directory
        else:
            print("Please enter a directory to use as input")

    def set_location(self, location):
        if not location:
            print("Please enter a location for output files to be saved")
            return

        print("Output location set to \"{location}\"".format(location=location))
        if not location.endswith("/") and not location.endswith("\\"):
            # make sure it is a directory
            if "\\" in location:    # pragma: no cover
                location = location + "\\"
            else:
                location = location + "/"   # pragma: no cover

        self.output_path = location

    def use_database(self, flag):
        if not self._check_input():
            return

        try:    # pragma: no cover
            if flag == "-i":
                self.db.insert_data(self.input_path)
            elif flag == "-v":
                filename = input("Enter a filename you would like to see the classes of: ")
                print(self.db.get_specific(filename))
            elif flag == "-r":
                filename = input("Enter a filename you would like to remove from the database: ")
                self.db.remove_data(filename)
            elif flag == "-a":
                print(self.db.get_all())
            elif flag == "":
                db_name = input("Enter a database name to connect to(or press Enter to use default): ")
                if db_name is "":
                    self.db.create_connection("uml_components.db")
                else:
                    self.db.create_connection(db_name)
            else:
                raise Exception("Not a valid flag")
        except Exception as err:    # pragma: no cover
            print("The exception is: ", err)
        return  # pragma: no cover

    def use_shelf(self, flag):
        if not self._check_input():
            return

        try:    # pragma: no cover
            if flag == '-w':
                    self.shelf.write_shelf(self.input_path)
            elif flag == '-r':
                key_name = input("Enter a filename(key) to read from shelf: ")
                if not key_name:
                    raise ValueError("You did not enter a key name")
                else:
                    print(self.shelf.read_selected_from_shelf(key_name))
            elif flag == '-a':
                print(self.shelf.read_shelf())
            elif flag == '-d':
                key_name = input("Enter a filename(key) to delete from shelf: ")
                if not key_name:
                    raise ValueError("You did not enter a key name")
                else:
                    self.shelf.delete_key_from_shelf(key_name)
                    print("[{key_name}] deleted successfully from shelf".format(key_name=key_name))
            elif flag == "":
                shelf_name = input("Enter a shelf name to use: ")
                if not shelf_name:
                    raise ValueError("You did not enter a name")
                else:
                    self.shelf.set_shelf(shelf_name)
                    print("Shelf [{shelf_name}] created successfully".format(shelf_name=shelf_name))
            else:
                raise Exception("Not a valid flag")
        except Exception as err:    # pragma: no cover
            print("The exception is: ", err)
        return  # pragma: no cover

    def make_pie_chart(self, params):
        if not self._check_run():
            return  # pragma: no cover
        if not params:
            print("Generating pie charts for all components")
            self.vg.generate_pie_charts()
            return
        if " " in params:   # pragma: no cover
            # split params into component name and output file
            comp_name, output_file_name = params.split(' ')
        else:
            comp_name = params
            output_file_name = None

        print("Generating a pie chart for component: {comp_name}".format(comp_name=comp_name))
        self.vg.generate_pie_chart(comp_name, output_file_name)

    def make_bar_chart(self, output_file_name):
        if self._check_run():
            if not output_file_name:
                output_file_name = None  # pragma: no cover
            self.vg.generate_bar_chart(output_file_name)
            print("Generating a bar chart")

    def _check_input(self):
        # removes duplication of this message in code
        if not self.input_path:
            print("Please select an input path with \"file\" or \"directory\"")
            return False

        return True

    def _check_run(self):
        """
        Check if the Umlify has been run, if not then return a message and false
        :return: True if run has been used, False if not
        """
        # removes duplication of this message in code
        if not self.run:
            print("Please use \"run\" before trying to create a chart")
            return False
        return True
