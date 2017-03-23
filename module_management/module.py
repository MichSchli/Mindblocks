class Module:

    manifest = {}
    components = []

    def __init__(self, manifest):
        self.manifest = manifest
        self.components = []

    def get_filtered_copy(self, view=None):
        copy = Module(manifest=self.manifest)
        for component in self.components:
            if view is None or view in component.manifest['views']:
                copy.add_component(component)
        return copy

    def add_component(self, component):
        self.components.append(component)

    def has_components(self):
        return len(self.components) > 0

    def get_name(self):
        return self.manifest['name']