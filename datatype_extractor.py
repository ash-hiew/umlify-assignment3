import re


class DataTypeExtractor:
    @staticmethod
    def _regex_search(regex, data):
        r = re.compile(regex)
        regex_result = r.findall(data)
        return regex_result

    def _extract_defaults_datatypes(self, line):
        attr_default = self._extract_attribute_defaults(line)
        attr_type = self._extract_attribute_datatypes(attr_default)
        def_data_types_dict = {attr_type: attr_default}
        return def_data_types_dict

    def _extract_attribute_defaults(self, line):
        regex = '\s{2}self\.\w+\s=\s(.*)'
        attribute_default = self._regex_search(regex, line)
        if attribute_default.__len__() != 0:
            attribute_default = attribute_default[0].replace('"', "")
        return attribute_default

    def _extract_attribute_datatypes(self, attr_name):
        regex = '^(.)'
        regex2 = '^[A-Z].+\)$'
        extracted_type = self._regex_search(regex, attr_name)
        data_type = extracted_type[0]
        if self._regex_search(regex2, attr_name):
            return 'obj'
        elif data_type.isalpha():
            return 'str'
        elif data_type == "'":
            return 'str'
        elif data_type == '{':
            return 'dict'
        elif data_type == '[':
            return 'list'
        elif data_type == '(':
            return 'tuple'
        elif data_type.isdigit():
            return "int"
        else:
            raise ValueError("No data type detected for '{0}'1".format(attr_name))