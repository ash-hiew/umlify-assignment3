from generators.diagram_generator import DiagramGenerator
from extractor import Extractor
from graphviz import ExecutableNotFound
from os import path, remove
from graphviz import Digraph


class UMLDiagramGenerator(DiagramGenerator):
    def __init__(self, input_path=None, output_path=None):
        super().__init__()
        self.input_path = input_path
        self.e = Extractor()
        if output_path:
            self.output_path = output_path
        if input_path:
            self.e.set_file(input_path)
            self.path_provided = True
        self.components = list(self.e.get_component_dictionary().values())
        self.error = ""

    def generate_class_diagram(self, output_file_name=None):
        dot = None
        if output_file_name is None:
            output_file_name = "class-diagram"
        output_file_name = self.output_path + output_file_name
        try:
            dot = self._initialise_diagram('UML Class Diagram', 'dot')
        except ExecutableNotFound:  # pragma: no cover
            raise Exception("Graphviz executable not found, please check it is properly installed.")
        if (len(self.components) > 0) & (dot is not None):
            for comp in self.components:
                dot = self._add_comp_to_diagram(dot, comp)
                dot = self._add_parents_to_diagram(dot, comp)
            dot.render(output_file_name, view=False)
            self.write_dot_to_png(dot_file=output_file_name)
            self._remove_temp_files(output_file_name)
        else:   # pragma: no cover
            print("unable to add components to diagram.")

    @classmethod
    def _initialise_diagram(cls, comment, diagram_format):
        dot = Digraph(comment=comment)
        dot.node_attr['shape'] = "record"
        dot.format = diagram_format
        return dot

    @classmethod
    def _add_parents_to_diagram(cls, dot, comp):
        for parent in comp.get_parents():
            dot.edge(parent.get_name(), comp.get_name())
            dot.edge_attr.update(dir="back")
            dot.edge_attr.update(arrowtail='empty')
        return dot

    @classmethod
    def _remove_temp_files(cls, output_file_name):
        if path.exists(output_file_name):
            remove(output_file_name)
        if path.exists(output_file_name + ".dot"):
            remove(output_file_name + ".dot")

    @classmethod
    def _build_record_string(cls, comp_name, attributes, functions):
        record = "{"
        record += "{name} | {attribs} |{functs}".format(name=comp_name, attribs=attributes,
                                                        functs=functions)
        record += "}"
        return record

    @classmethod
    def _add_comp_to_diagram(cls, dot, comp):
        comp_name = comp.get_name()
        attributes = cls._build_attributes_string(comp.get_attributes())
        functions = cls._build_function_string(comp.get_functions())
        record = cls._build_record_string(comp_name, attributes, functions)
        dot.node(comp_name, record)
        return dot

    @classmethod
    def _build_function_string(cls, functions):
        function_string = ""
        for funct in functions:
            function_string += funct + "\\n"
        return function_string

    @classmethod
    def _build_attributes_string(cls, attributes):
        attribute_string = ""
        for attrib in attributes:
            attribute_string += attrib
            for a in attributes[attrib]:
                attribute_string += " : " + a
            attribute_string += "\\n"
        return attribute_string
