class Plant:

    def __init__(self, h=10):
        self.plant_height = h

    def grow_plant(self):
        pass


class Sunflower(Plant):

    def __init__(self):
        self.seed = Seed()

    def drop_seed(self):
        pass


class Orchid(Plant):
    pass

class Seed(object):
    pass
