from unittest import TestCase, main, skip, mock
import io
from extractor import Extractor
from component import Component
from os import path, rename, makedirs
from shutil import rmtree
from visual_generator import VisualGenerator


class UCVTests(TestCase):
    """Tests for VisualGenerator.py, ChartGenerator, DiagramGenerator"""

    def setUp(self):
        if path.exists("output"):
            rmtree("output")
        self.test_file = "./tests/test_class_5.py"
        self.vg = VisualGenerator(self.test_file)
        self.components = list(self.vg.comp_dict.values())
        self.comp = Component()
        self.comp.set_name("Herbivore")
        att_dict = {'teeth': {'str': 'sharp'}, 'eyes': {'int': '2'}, 'genus': {'dict': '{}'}, 'skin': {'str': 'furry'}}
        self.comp.set_attributes(att_dict)

        self.components.append(self.comp)

    def tearDown(self):
        if path.exists("output"):
            rmtree("output")
        if path.exists(".\\temp"):
            rename(".\\temp", ".\\graphviz")
        if path.exists(".\\temp2"):
            rmtree(".\\graphviz")
            rename(".\\temp2", ".\\graphviz")

    def test_file_path(self):
        self.assertEqual(self.test_file, self.vg.input_path)

    def test_extractor(self):
        self.assertIsInstance(self.vg.e, Extractor)

    def test_components_not_none(self):
        self.assertIsNotNone(self.components)

    def test_components_not_empty(self):
        self.assertIsNot(len(self.components), 0)

    def test_components_is_list(self):
        self.assertIsInstance(self.components, list)

    def test_components_initialised(self):
        empty_comp = VisualGenerator(output_path='output/')
        self.assertEqual(len(empty_comp.comp_dict.values()), 0)

    def test_components_list_components(self):
        comps = self.components
        test_item = comps[0]
        self.assertIsInstance(test_item, Component)

    def test_get_attribute_types(self):
        expected_types = {'dict': 1, 'int': 1, 'list': 0, 'object': 0, 'str': 2, 'tuple': 0}
        att_types = self.vg.pie_chart_gen._get_attribute_types(self.comp)
        self.assertEqual(expected_types, att_types)

    def test_get_attribute_types_without_component(self):
        expected_types = {'dict': 0, 'int': 0, 'list': 0, 'object': 0, 'str': 0, 'tuple': 0}
        att_types = self.vg.pie_chart_gen._get_attribute_types(component=None)
        self.assertEqual(expected_types, att_types)

    def test_get_attribute_types_without_attributes(self):
        expected_types = {'dict': 0, 'int': 0, 'list': 0, 'object': 0, 'str': 0, 'tuple': 0}
        self.comp.set_attributes(None)
        att_types = self.vg.pie_chart_gen._get_attribute_types(self.comp)
        self.assertEqual(expected_types, att_types)

    def test_get_attribute_types_with_empty_attributes(self):
        expected_types = {'dict': 0, 'int': 0, 'list': 0, 'object': 0, 'str': 0, 'tuple': 0}
        att_dict = {'teeth': {'': 'sharp'}}
        self.comp.set_attributes(att_dict)
        att_types = self.vg.pie_chart_gen._get_attribute_types(self.comp)
        self.assertEqual(expected_types, att_types)

    def test_generate_pie_chart(self):
        self.vg.e.component_dict[self.comp.get_name()] = self.comp
        self.vg.pie_chart_gen._get_attribute_types(self.comp)
        self.vg.generate_pie_chart("Herbivore", '')
        fname = "output\\Herbivore-pie-chart.png"
        self.assertTrue(path.isfile(fname))

    def test_generate_pie_chart_without_component(self):
        self.vg.generate_pie_chart("Hello", '')
        fname = "output\\Hello-pie-chart.png"
        self.assertFalse(path.isfile(fname))

    def test_generate_pie_chart_with_output_file_name(self):
        self.vg.e.component_dict[self.comp.get_name()] = self.comp
        self.vg.pie_chart_gen._get_attribute_types(self.comp)
        self.vg.generate_pie_chart("Herbivore", output_file_name='Herbivore-pie-chart')
        fname = "output\\Herbivore-pie-chart.png"
        print(path.dirname(fname))
        self.assertTrue(path.isfile(fname))

    def test_generate_class_diagram(self):
        self.vg.generate_diagram()
        fname = 'output\\class-diagram.png'
        self.assertTrue(path.isfile(fname))

    def test_generate_class_diagram_without_components(self):
        self.vg.components = []
        self.vg.diagram_gen.generate_class_diagram(output_file_name='class-diagram.png')
        fname = 'output\\class-diagram.png'
        self.assertFalse(path.isfile(fname))

    def test_generate_pie_charts(self):
        self.vg.e.component_dict[self.comp.get_name()] = self.comp
        self.vg.pie_chart_gen._get_attribute_types(self.comp)
        fname = "output\\Herbivore-pie-chart.png"
        self.vg.generate_pie_charts()
        self.assertTrue(path.isfile(fname))

    def test_generate_bar_chart(self):
        fname = "output\\bar-chart.png"
        self.vg.generate_bar_chart(None)
        self.assertTrue(path.isfile(fname))

    def test_generate_bar_chart_with_output_path_created(self):
        fname = "output\\bar-chart.png"
        makedirs("output")
        self.vg.generate_bar_chart(None)
        self.assertTrue(path.isfile(fname))

    def test_remove_temp_files(self):
        fname = 'output\\class-diagram'
        self.vg.diagram_gen._remove_temp_files(fname)
        self.assertFalse(path.isfile(fname))

    def test_generate_bar_chart_without_object(self):
        self.vg.comp_dict = {}
        expected = "unable to generate bar chart, no components found\n"

        # Act
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            self.vg.generate_bar_chart(output_file_name='bar-chart')
        # Assert
        self.assertEqual(expected, fake_stdout.getvalue())


if __name__ == '__main__':
    main(verbosity=2)
