import sqlite3 as sql
import pickle
from extractor import Extractor
import os


class Database:
    def __init__(self):
        self._conn = None
        self._cursor = None
        self.db_name = None
        self.file_path = None

    def create_connection(self, file_name="uml_components.db"):
        """Create a connection to SQLite Database"""
        if file_name is not None:
            self.file_path, self.db_name = os.path.split(file_name)
            if self.file_path != "":
                self.file_path += "/"
            self._conn = sql.connect(self.file_path + self.db_name)
            self._cursor = self._conn.cursor()
            print("Connected to database")
            print("Database created")
            self.create_table()
        else:
            raise sql.Error("An Error occurred.")
        self.close_connection()

    def query(self, sql_command, parameters=None):
        try:
            self._conn = sql.connect(self.file_path + self.db_name)
            self._cursor = self._conn.cursor()
            if parameters is None:
                self._cursor.execute(sql_command)
            else:
                try:
                    self._cursor.execute(sql_command, parameters)
                except sql.IntegrityError:
                    print("Duplication Error: file has already been added")
                    return False
            self._conn.commit()
            return True
        except TypeError:
            print("Please connect to a database first")
            return False
        except (sql.Error, FileNotFoundError) as e:  # pragma: no cover
            self.close_connection()
            print('Error:', e)
            return False

    def close_connection(self):
        if self._conn is not None:
            self._conn.close()
        else:
            return False

    def get_db_info(self):
        """Displays the name of current database and the number of pickled files"""
        self.query("select count(*) from classes")
        result = str(self._cursor.fetchone()[0])

        output = "Selected Database: " + self.db_name + "\n"
        output += "The number of pickled files in the database: " + result

        self.close_connection()

        return output

    @classmethod
    def extract_data(cls, file):
        """"Uses extraction method from Extractor class"""
        ext = Extractor()
        ext.set_file(file)
        return ext.get_component_dictionary()

    def drop_table(self):
        """Drop a table called classes in the database"""
        if self.query("DROP TABLE IF EXISTS classes"):  # pragma: no cover
            print("table dropped from database")

        self.close_connection()

    def create_table(self):
        """Create a table called classes to the database"""
        sql_command = """
            CREATE TABLE IF NOT EXISTS classes (
            filename VARCHAR(20) PRIMARY KEY,
            pickled_dict BLOB);"""
        if self.query(sql_command):  # pragma: no cover
            print("table created for database " + self.db_name)

        self.close_connection()

    def insert_data(self, selected_file):
        """Add pickled component data to database"""
        filename = os.path.basename(selected_file).strip('.py')
        comp_dict = self.extract_data(selected_file)
        if not comp_dict:
            print("Cannot add", filename, "to database")
        else:
            pickled_file = pickle.dumps(comp_dict, pickle.HIGHEST_PROTOCOL)
            sql_command = "INSERT INTO classes(filename, pickled_dict) VALUES(?, ?)"
            if self.query(sql_command, (filename, sql.Binary(pickled_file))):
                print("Components pickled and inserted into database")

        self.close_connection()

    def remove_data(self, selected_file):
        """Remove pickled data from database"""

        filename = os.path.basename(selected_file).strip('.py')
        sql_command = "DELETE FROM classes WHERE filename=?"
        self.query(sql_command, (filename,))
        print("[%s] components removed from database" % filename)
        # print("Cannot remove", selected_file, "from database")

        self.close_connection()

    def get_specific(self, selected_file):
        """Display component data of selected filename from database"""
        _conn = None
        unpickled_dict = {}

        if '.py' in selected_file:
            filename = os.path.basename(selected_file).strip('.py')
        else:
            filename = os.path.basename(selected_file)

        # return value
        output = ""
        new_line = "\n"
        format_str = "SELECT filename, pickled_dict from classes where filename='{filename}';"
        sql_command = format_str.format(filename=filename)

        self.query(sql_command)

        for filename, pickled_dict in self._cursor.fetchall():
            unpickled_dict = pickle.loads(pickled_dict)
        for class_name, class_data in unpickled_dict.items():
            output += "Class Name:" + class_data.name + new_line
            output += "Attribute:" + str(class_data.get_attributes()) + new_line
            output += "Function:" + str(class_data.get_functions()) + new_line
            for parent in class_data.parents:  # pragma: no cover
                output += "Parent:" + parent.name + new_line
            output += "-" * 20 + new_line

        self.close_connection()
        return output

    def get_all(self):
        """Display all component data from database"""
        # return value
        output = ""
        count = 0
        new_line = "\n"
        sql_command = "SELECT filename, pickled_dict from classes;"

        self.query(sql_command)

        for filename, pickled_dict in self._cursor.fetchall():
            unpickled_dict = pickle.loads(pickled_dict)
            for class_name, class_data in unpickled_dict.items():
                output += "Class Name:" + class_data.name + new_line
                output += "Attribute:" + str(class_data.get_attributes()) + new_line
                output += "Function:" + str(class_data.get_functions()) + new_line
                for parent in class_data.parents:
                    output += "Parent:" + parent.name + new_line
                output += "-" * 20 + new_line
                count += 1
        output += "The number of components in the database: " + str(count)
        return output


if __name__ == "__main__":  # pragma: no cover
    import doctest
    doctest.testmod(verbose=True)
