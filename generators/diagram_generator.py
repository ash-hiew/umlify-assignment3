from abc import ABC
from abc import abstractmethod
from os import path, environ, pathsep, makedirs

from pydot import graph_from_dot_file


class DiagramGenerator(ABC):

    def __init__(self, graphviz=None):
        self.dot_class_file = "class-diagram.dot"
        if graphviz is None:
            self.path_to_graphviz = "graphviz/release/bin"
        else:   # pragma: no cover
            self.path_to_graphviz = graphviz
        self.output_path = "output/"
        self.setup()

    def setup(self, new_path_to_graphviz=None):
        """
        Method to setup the path to dot.exe on the executing computer. Used for both pydot or
        pyreverse pretty printing.
        :param new_path_to_graphviz: the full path to dot.exe. If no path is
        provided, assumes the graphviz source is in the working directory under graphviz and
        sets the path to that.
        """
        if new_path_to_graphviz is None:    # pragma: no cover
            dir_path = path.dirname(path.realpath(__file__))
            full_path = path.join(dir_path, self.path_to_graphviz)
            new_path_to_graphviz = path.normcase(full_path)

        environ["PATH"] += pathsep + new_path_to_graphviz

    @abstractmethod
    def generate_class_diagram(self):
        pass    # pragma: no cover

    def write_dot_to_png(self, dot_file, output=None):
        """
        Method to take a dot image definition file and convert it to a png
        :param dot_file: the name of the dot file without the .dot extension
        :param output: the name of the output file without the .png extension.
                if no output_file_name provided, will produce input_file_name.png
        """
        # reference: https://stackoverflow.com/questions/5316206/converting-dot-to-png-in-python
        if dot_file is None:    # pragma: no cover
            dot_file = self.dot_class_file

        if dot_file is not None:    # pragma: no cover
            if not path.exists(self.output_path):
                makedirs(self.output_path)
            if output is None:
                output = dot_file
            if not output.endswith(".png"):
                if output.endswith(".", -4, -3):
                    output = output[:-3] + "png"    # pragma: no cover
                else:
                    output = output + ".png"
            try:
                (graph,) = graph_from_dot_file("{file}".format(file=dot_file))
                graph.write_png("{file}".format(file=output))
                return "file: {file} successfully converted to {result}".format(file=dot_file, result=output)

            except FileNotFoundError as err:
                print("Couldn't find the files necessary to perform the conversion.")
                print("Please provide path to dot.exe and the .dot file to convert")
                print(err)
        else:
            return "No dot file provided to convert"    # pragma: no cover
