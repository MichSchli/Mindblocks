import json
import os

from model.module.module_model import ModuleModel
from model.module.toolbox_item.toolbox_item_specifications import ToolboxItemSpecifications
from observables.observable_dictionary import ObservableDict


class ModuleRepository:

    modules = None
    component_dir = '/home/michael/Projects/Mindblocks/packages'

    def __init__(self, prototype_repository):
        self.prototype_repository = prototype_repository
        self.modules = ObservableDict()

    def get_basic_modules(self, specification):
        if specification.package_name is None:
            specification.package_name = self.get_all_package_names()

        modules = []

        for package_name in specification.package_name:
            module = self.get_basic_module_by_package_name(package_name)
            modules.append(module)

        return modules


    def get_basic_module_by_package_name(self, package_name):
        manifest = self.load_package_manifest(package_name)
        module = ModuleModel(manifest)

        prototype_specifications = ToolboxItemSpecifications()
        prototype_specifications.package_manifest = manifest

        prototypes = self.prototype_repository.get_prototypes(prototype_specifications)
        module.extend_prototypes(prototypes)

        return module

    def get_canvas_modules(self):
        return []

    '''
    Logic for loading modules:
    '''
    def get_all_package_names(self):
        all_subitems = os.listdir(self.component_dir)
        filtered_subitems = [item for item in all_subitems if self.filter_name(item)]

        absolute_subitems = [(d,os.path.join(self.component_dir, d)) for d in filtered_subitems]
        subfolders = [d[0] for d in absolute_subitems if os.path.isdir(d[1])]

        return subfolders

    def filter_name(self, name):
        if name.startswith('.') or name.startswith('_'):
            return False

        return True

    def load_manifest(self, path):
        manifest_path = os.path.join(path, 'manifest.json')
        with open(manifest_path) as data_file:
            manifest = json.load(data_file)
            manifest['path'] = path
            return manifest

    def load_package_manifest(self, package_name):
        manifest_path = os.path.join(self.component_dir, package_name)
        manifest = self.load_manifest(manifest_path)
        manifest['package'] = package_name
        return manifest