from generators.chart_generator import ChartGenerator
import matplotlib.pyplot as plt
from numpy import arange


class BarChartGenerator(ChartGenerator):
    def __init__(self, comp_dict):
        ChartGenerator.__init__(self)
        self.comp_dict = comp_dict
        self.no_of_attributes = []
        self.no_of_functions = []
        self.objects = None
        self.chart_type = 'bar-'

    def prepare_chart_details(self):
        objects = tuple(self.comp_dict.keys())
        self.objects = objects
        self.flag = len(objects)
        for key in objects:
            component = self.comp_dict.get(key)
            self.no_of_attributes.append(len(component.get_attributes()))
            self.no_of_functions.append(len(component.get_functions()))

    def set_chart_type_with_details(self):
        bar_width = 0.35
        opacity = 0.8

        y_pos = arange(len(self.objects))

        plt.bar(y_pos, self.no_of_attributes, bar_width, alpha=opacity, color='b', label='attributes')
        plt.bar(y_pos + bar_width, self.no_of_functions, bar_width, alpha=opacity, color='g', label='functions')
        plt.xticks(y_pos + bar_width, self.objects, rotation=90)
        plt.subplots_adjust(bottom=0.50)
        plt.ylabel('Count')
        plt.xlabel('Class Name')
        plt.legend()

    def set_chart_title(self):
        plt.title('Number of Functions and Attributes per Class')
