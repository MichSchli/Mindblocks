import importlib
import inspect
import os

from importer.imported_component import ImportedComponent
from importer.imported_module import ImportedModule

class Importer:

    component_dir = 'components'

    def __init__(self):
        pass

    def import_modules(self):
        modules = [ImportedModule(*d) for d in self.get_category_folders()]
        for module in modules:
            self.fill_module(module)
        return modules

    def filter_name(self, name):
        if name.startswith('.') or name.startswith('_'):
            return False

        return True

    def get_category_folders(self):
        all_subitems = os.listdir(self.component_dir)
        filtered_subitems = [item for item in all_subitems if self.filter_name(item)]
        absolute_subitems = [(d,os.path.join(self.component_dir, d)) for d in filtered_subitems]
        subfolders = [d for d in absolute_subitems if os.path.isdir(d[1])]

        return subfolders

    def fill_module(self, module):
        component_files = module.manifest['files']
        for file in component_files:
            path = os.path.join(module.path, file['name'])
            loaded_file = importlib.machinery.SourceFileLoader("module", path).load_module()

            for component in file['components']:
                component_class = getattr(loaded_file, component['name'])
                module.add_component(ImportedComponent(component, component_class))