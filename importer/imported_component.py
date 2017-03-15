import inspect

class ImportedComponent:

    def __init__(self, manifest, component_class):
        self.manifest = manifest
        self.component_class = component_class
        self.component_class.module = manifest['file_path']


