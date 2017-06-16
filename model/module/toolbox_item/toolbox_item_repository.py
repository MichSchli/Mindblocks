import importlib
import os

from model.module.toolbox_item.toolbox_item_model import ToolboxItemModel
from observables.observable_dictionary import ObservableDict


class ToolboxItemRepository:

    component_dir = '/home/michael/Projects/Mindblocks/packages'

    defined_toolbox_prototypes = None

    def __init__(self):
        self.defined_toolbox_prototypes = ObservableDict()

    def get(self, specifications):
        for element in self.defined_toolbox_prototypes.elements.values():
            if specifications.matches(element):
                return element

    def get_prototypes(self, specifications):
        if specifications.package_manifest is not None:
            return self.get_prototypes_by_package_manifest(specifications.package_manifest)

    def load_prototypes(self, package_manifest):
        component_files = package_manifest['files']
        module_path = package_manifest['module_name']

        prototypes = []

        for file_manifest in component_files:
            os_path = os.path.join(package_manifest['path'], file_manifest['name'])
            class_path = module_path + "." + file_manifest['name'].split(".")[0]
            loaded_file = importlib.machinery.SourceFileLoader("module", os_path).load_module()

            for component_manifest in file_manifest['components']:
                component_manifest['file_path'] = class_path
                component_manifest['package'] = package_manifest['package']
                component_class = getattr(loaded_file, component_manifest['name'])

                prototype = ToolboxItemModel()
                prototype.name = component_manifest['name']
                prototype.package = package_manifest['package']
                prototype.prototype_class = component_class
                prototype.attributes = component_class.default_attributes
                prototypes.append(prototype)

                self.defined_toolbox_prototypes.append(prototype)

        return prototypes