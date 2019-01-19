from controller import InterpreterController
from database import Database
from shelf import Shelf
from interpreter import Interpreter


if __name__ == '__main__':
    database = Database()
    shelf = Shelf()
    interpreter = Interpreter()
    controller = InterpreterController(interpreter, database, shelf)
    interpreter.attach(controller)
    controller.start()
