
class Mammal(object):
    """ Test Python file for file extractor"""
    def feeds(self):
        print ("milk")
    def proliferates(self):
        pass

class Marsupial(Mammal):
        def proliferates(self):
            print("poach")

class Eutherian(Mammal):
        def proliferates(self):
            print("placenta")

class Carnivore(Mammal):
        def __init__(self):
            self.teeth = "sharp"
            self.eyes = 2

        def proliferates(self):
            print("meat eater")

class Herbivore(Mammal):
        def __init__(self):
            self.teeth = "blunt"
            self.skin = "furry"
            self.genus = {}

        def proliferates(self):
            print("plant eater")

