# Inheritance Test Data
class Person:

    def __init__(self, new_name, new_age):
        self.name = new_name
        self.age = new_age


class Employee(Person):
    def __init__(self, new_name, new_age, new_staff_num):
        super().__init__(new_name, new_age)
        self.staff_number = new_staff_num
