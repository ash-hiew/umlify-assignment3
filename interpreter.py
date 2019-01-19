"""
This module handles the command line input and help messages for Umlify.
This is the model part of the MVC architecture.
Handles the flow of data from the various modules
"""

from cmd import Cmd
from abc import ABCMeta


class Subject(metaclass=ABCMeta):
    def __init__(self):
        self.subscribers = list()
        self.command = False
        self.input = None

    def attach(self, observer):
        self.subscribers.append(observer)

    def detach(self, observer):
        self.subscribers.remove(observer)

    def notify(self):
        for sub in self.subscribers:
            sub.update()

    def set_state(self, command, arg):
        self.command = command
        self.input = arg
        self.notify()

    def get_command(self):
        return self.command

    def get_input(self):
        return self.input


# Model
class Interpreter(Cmd, Subject):
    """
    Interpreter class that uses Cmd and inherits from Subject
    Instead of a single command with multiple options (eg `umlify -d ./myclasses/ -o image.png`
    it will have multiple commands to set each value
    """

    def __init__(self):
        Cmd.__init__(self)
        Subject.__init__(self)
        self.prompt = "Umlify> "
        self.intro = "Welcome to Umlify - UML Diagram generator. Use \"help\" for help."
        self.run = False

    def do_run(self, arg=''):
        self.run = True
        self.set_state("run", arg)

    def do_bar_chart(self, output_file_name=''):
        self.set_state("bar_chart", output_file_name)

    def do_pie_chart(self, arg=''):
        self.set_state("pie_chart", arg)

    def do_file(self, arg=''):
        self.set_state("file", arg)

    def do_directory(self, arg=''):
        self.set_state("directory", arg)

    def do_location(self, arg=''):
        self.set_state("location", arg)

    def do_type(self, arg=''):
        self.set_state("type", arg)

    def do_shelf(self, arg=''):
        self.set_state("shelf", arg)

    def do_database(self, arg=''):
        self.set_state("database", arg)

    @staticmethod
    def help_run():
        print("""
        Usage: run
        Runs Umlify with the current settings, use other commands to change them
        :return:
        """)

    @staticmethod
    def help_bar_chart():
        print("""
    Usage: bar_chart [output_file_name]
    Generate a bar chart about classes
    :param output_file_name: the file name for the chart to output to
    :return:
    """)

    @staticmethod
    def help_pie_chart():
        print("""
    Usage: pie_chart [comp_name] [output_file_name]
    Makes a pie chart about a class. Give no input for pie charts of every component
    :param params: the input which includes optional values comp_name and output_file_name
    comp_name the name of the component to make a chart of
    output_file_name the file name for the chart to output to
    :return:
    """)

    @staticmethod
    def help_file():
        print("""
    Usage: file <file>
    Selects a file as input to Umlify
    :param file: the name of the file to be used as input
    :return: None
    """)

    @staticmethod
    def help_directory():
        print("""
    Usage: directory <directory>
    Selects a directory as input to Umlify
    :param directory: the name of the directory holding files to be used as input
    :return: None
    """)

    @staticmethod
    def help_location():
        print("""
    Usage: location <location>
    Selects a location to output the files
    :param location: the name of the location to be used as output
    :return: None
    """)

    @staticmethod
    def help_type():
        print("""
    Usage: type <file_type>
    Sets the output file type
    Allowed types: "dot", "png", "pdf"
    :param file_type: a string representing a file extension
    :return: None
    """)

    @staticmethod
    def help_shelf():
        print("""
        Writes and reads Component objects extracted from the currently selected file to [filename].shelve

        Usage: shelf <flag> OR s <flag>
        shelf: User will be prompted to enter a shelf name
        shelf -w: writes the class components of selected file to [shelf_name].shelve
        shelf -a: reads all the contents of shelve file
                  User will be prompted to input name of shelve file
        shelf -r: loads a specific key from the shelve
                  User will be prompted to input name of key
        shelf -d: Deletes a specific key from shelve file
                  User will be prompted to input key
        :param flag: -w, -r, -a, -d
        :return: shelf values
        """)

    @staticmethod
    def help_database():
        print("""
        Save and read class component data with a database. Stores component object as a pickle file.

        Usage: database <flag> OR db <flag>
        db: User will be prompted to enter a database name
        db -i: inserts the class components of currently selected file to the database
        db -d: remove the class components of a selected file in the database
                User will be prompted to enter a filename
        db -v: displays the class components of a certain filename within the database
               User will be prompted to enter a filename
        db -a: displays all data and the number of components stored in the database

        :param flag: -i, -v, -d, -a
        :return: db values
        """)

    @staticmethod
    def help_quit():
        print("""
                Usage: quit
                Quit Umlify
                :return: True
                """)

    @staticmethod
    def do_quit():
        print("Quitting Umlify...")
        return True

    # command aliases
    do_r = do_run
    help_r = help_run
    do_b = do_bar_chart
    help_b = help_bar_chart
    do_p = do_pie_chart
    help_p = help_pie_chart
    do_f = do_file
    help_f = help_file
    do_d = do_directory
    help_d = help_directory
    do_l = do_location
    help_l = help_location
    do_t = do_type
    help_t = help_type
    do_s = do_shelf
    help_s = help_shelf
    do_db = do_database
    help_db = help_database
    do_q = do_quit
    help_q = help_quit

