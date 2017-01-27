import json
import os

class ImportedModule:

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.components = []

        self.manifest = self.load_manifest()

    def get_name(self):
        return self.name

    def load_manifest(self):
        manifest_path = os.path.join(self.path, 'manifest.json')
        with open(manifest_path) as data_file:
            return json.load(data_file)

    def add_component(self, component):
        self.components.append(component)