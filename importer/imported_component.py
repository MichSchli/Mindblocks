import inspect

class ImportedComponent:

    def __init__(self, manifest, component_class):
        self.manifest = manifest
        self.component_class = component_class

        self.set_source_lines()

    def set_source_lines(self):
        source_string = inspect.getsourcelines(self.component_class.compile_theano)
        self.component_class.source_string = source_string



