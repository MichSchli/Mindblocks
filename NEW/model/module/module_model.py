class ModuleModel:

    manifest = None
    name = None
    components = []

    def __init__(self, manifest):
        self.manifest = manifest
        self.name = manifest['name']
        self.components = []

    def get_name(self):
        return self.name

    def get_components(self):
        return self.components

    def has_components(self):
        return len(self.components) > 0

    def extend_prototypes(self, prototypes):
        self.components.extend(prototypes)