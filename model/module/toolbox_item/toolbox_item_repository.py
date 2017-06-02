import importlib
import os

from model.module.toolbox_item.toolbox_item_model import ToolboxItemModel


class ToolboxItemRepository:

    component_dir = '/home/michael/Projects/Mindblocks/packages'

    def get_prototypes(self, specifications):
        if specifications.package_manifest is not None:
            return self.get_prototypes_by_package_manifest(specifications.package_manifest)

    def get_prototypes_by_package_manifest(self, package_manifest):
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
                prototype.prototype_class = component_class
                prototype.attributes = component_class.default_attributes
                prototype.manifest = component_manifest
                prototypes.append(prototype)
        return prototypes