

class IdentifierFactory:

    name_directory = {}

    def __init__(self):
        self.name_directory = {}

    def get_next_identifier(self, name_string="default", separator='_'):
        if name_string in self.name_directory:
            value = self.name_directory[name_string] + 1
        else:
            value = 0

        self.name_directory[name_string] = value

        return name_string + separator + str(value)

    def assign_identifier(self, identifiable):
        name = identifiable.get_name()
        identifier = self.get_next_identifier(name)
        identifiable.set_unique_identifier(identifier)