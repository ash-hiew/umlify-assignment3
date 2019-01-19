from generators.uml_diagram_generator import UMLDiagramGenerator
from generators.pie_chart_generator import PieChartGenerator
from generators.bar_chart_generator import BarChartGenerator
from extractor import Extractor


class VisualGenerator(object):
    def __init__(self,  input_path=None, output_path=None):
        self.e = Extractor()
        if input_path:
            self.e.set_file(input_path)
        self.comp_dict = self.e.get_component_dictionary()
        self.input_path = input_path
        self.output_path = output_path
        self.diagram_gen = UMLDiagramGenerator(input_path, output_path)
        self.pie_chart_gen = PieChartGenerator(self.comp_dict)
        self.bar_chart_gen = BarChartGenerator(self.comp_dict)

    def generate_diagram(self):
        self.diagram_gen.generate_class_diagram(self.output_path)

    def generate_pie_chart(self, comp_name, output_file_name):
        self.pie_chart_gen.generate_chart(output_file_name, comp_name)

    def generate_pie_charts(self):
        for comp in self.comp_dict.keys():
            if comp != "":  # pragma: no cover
                self.pie_chart_gen.generate_chart(output_file_name='', comp_name=comp)

    def generate_bar_chart(self, output_file_name):
        if len(self.comp_dict.items()) > 0:
            self.bar_chart_gen.generate_chart(output_file_name)
        else:
            print("unable to generate bar chart, no components found")
