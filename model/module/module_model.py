from model.identifiables.identifiable import Identifiable


class ModuleModel(Identifiable):

    manifest = None
    name = None
    components = []

    def __init__(self, name):
        Identifiable.__init__(self, unique_identifier="module:"+name)
        self.name = name
        self.components = []

    def get_name(self):
        return self.name

    def get_components(self):
        return self.components

    def has_components(self):
        return len(self.components) > 0

    def extend_prototypes(self, prototypes):
        self.components.extend(prototypes)

    def get_prototype(self, identifier):
        for prototype in self.components:
            if prototype.name == identifier:
                return prototype

        return None