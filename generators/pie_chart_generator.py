from generators.chart_generator import ChartGenerator
import matplotlib.pyplot as plt


class PieChartGenerator(ChartGenerator):
    def __init__(self, comp_dict):
        ChartGenerator.__init__(self)
        self.comp_dict = comp_dict
        self.att_types = {}
        self.chart_type = 'pie-'

    def prepare_chart_details(self):
        att_types = {}
        self.comp_name = self.comp_name[0].upper() + self.comp_name[1:]
        the_component = self.comp_dict.get(self.comp_name)
        if the_component is not None:
            att_types = self._get_attribute_types(the_component)
            removable = []
            for k, v in att_types.items():
                if v == 0:
                    removable.append(k)
            for r in removable:
                att_types = self._remove_by_key(att_types, r)
        self.att_types = att_types
        self.flag = len(self.att_types)

    def set_chart_type_with_details(self):
        labels = self.att_types.keys()
        sizes = self.att_types.values()
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')

    def set_chart_title(self):
            plt.title("Percentage of variable data types")

    @classmethod
    def _get_attribute_types(cls, component):
        att_types = {"int": 0, "str": 0, "dict": 0, "list": 0, "tuple": 0, "object": 0}
        if component is not None:
            attributes = component.get_attributes()

            if attributes is not None:
                if len(attributes) > 0:
                    for attrib in attributes:
                        for a in attributes[attrib]:
                            if a is not '':
                                att_types[a] = att_types[a] + 1
        return att_types

    @classmethod
    def _remove_by_key(cls, dictionary, key):
        r = dict(dictionary)
        del r[key]
        return r
