class DataNode:
    def __init__(self, type_name):
        self.type_name = type_name
        self.fields = {}  # dict: field_name -> value