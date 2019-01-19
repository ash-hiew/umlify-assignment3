from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt
from os import path, makedirs


class ChartGenerator(metaclass=ABCMeta):
    def __init__(self):
        self.output_path = 'output/'
        self.output_file_name = ''
        self.chart_type = ''
        self.comp_name = ''
        self.flag = 0

    def generate_chart(self, output_file_name=None, comp_name=None):
        self.set_output_file_name(output_file_name, comp_name)
        self.prepare_chart_details()
        if self.flag > 0:
            self.set_chart_type_with_details()
            self.set_chart_title()
            self.build_chart()

    def set_output_file_name(self, output_file_name, comp_name):
        if not path.exists(self.output_path):
            makedirs(self.output_path)

        chart_type = self.chart_type + 'chart'

        if output_file_name is None and comp_name is None:
            self.output_file_name = chart_type
        else:
            self.output_file_name = output_file_name

        if output_file_name is '' and comp_name is not None:
            self.output_file_name = comp_name + '-' + chart_type
        elif output_file_name is not None and comp_name is not None:
            self.output_file_name = output_file_name

        self.comp_name = comp_name

    @abstractmethod
    def prepare_chart_details(self):
        pass    # pragma: no cover

    @abstractmethod
    def set_chart_type_with_details(self):
        pass    # pragma: no cover

    @abstractmethod
    def set_chart_title(self):
        pass    # pragma: no cover

    def build_chart(self):
        plt.savefig(self.output_path + self.output_file_name + '.png')
        plt.gcf().clear()
