import re


class ComponentExtractor:
    @staticmethod
    def _regex_search(regex, data):
        r = re.compile(regex)
        regex_result = r.findall(data)
        return regex_result

    def _extract_class(self, line):
        regex = '^class\s(\w+)'
        result = self._regex_search(regex, line)
        return result

    def _extract_parents(self, line):
        dependency_list = []
        regex = '^class\s\w+\((.*)\)'
        if not self._regex_search(regex, line):
            return ""
        else:
            dependency_names = self._regex_search(regex, line)[0]
            regex_list = (re.split(r',', dependency_names))
            for item in regex_list:
                if item != 'object':
                    stripped_item = item.strip()
                    dependency_list.append(stripped_item)
            return dependency_list

    def _extract_functions(self, line):
        regex = 'def\s(\w+)'
        return self._regex_search(regex, line)

    def _extract_attributes(self, line):
        regex = '\s{2}self\.(\w+)'
        return self._regex_search(regex, line)

