class Field:
    def __init__(self, name, field_type):
        self.name = name
        self.type = field_type


class Schema:
    def __init__(self, name):
        self.name = name
        self.fields = {}

    def add_field(self, field):
        self.fields[field.name] = field