class Component(object):

    def __init__(self):
        self.parents = []
        self.name = ''
        self.functions = []
        self.attributes = []

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_attributes(self, attributes):
        self.attributes = attributes

    def set_functions(self, functions):
        self.functions = functions

    def get_functions(self):
        return self.functions

    def get_attributes(self):
        return self.attributes

    def set_parents(self, parents):
        self.parents = parents

    def get_parents(self):
        return self.parents
