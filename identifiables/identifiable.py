
class Identifiable:

    unique_identifier = None
    name = None

    def __init__(self, unique_identifier=None, name=None):
        self.unique_identifier = unique_identifier
        self.name = name

    def get_unique_identifier(self):
        return self.unique_identifier

    def get_name(self):
        return self.name

    def set_unique_identifier(self, unique_identifier):
        self.unique_identifier = unique_identifier
