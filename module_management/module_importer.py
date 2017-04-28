import importlib
import inspect
import os
import json

from module_management.module import Module
from module_management.module_component import ModuleComponent


class ModuleImporter:

    component_dir = '/home/michael/Projects/Mindblocks/components'

    def import_modules(self):
        modules = []

        for module_path in self.get_category_folders():
            manifest = self.load_package_manifest(module_path)
            module = Module(manifest)
            self.add_components(module)
            self.fill_components(module)
            modules.append(module)

        return [m for m in modules if m.has_components()]

    def filter_name(self, name):
        if name.startswith('.') or name.startswith('_'):
            return False

        return True

    def get_category_folders(self):
        all_subitems = os.listdir(self.component_dir)
        filtered_subitems = [item for item in all_subitems if self.filter_name(item)]

        absolute_subitems = [(d,os.path.join(self.component_dir, d)) for d in filtered_subitems]
        subfolders = [d[0] for d in absolute_subitems if os.path.isdir(d[1])]

        return subfolders

    def add_components(self, module):
        component_files = module.manifest['files']
        module_path = module.manifest['module_name']

        for file_manifest in component_files:
            os_path = os.path.join(module.manifest['path'], file_manifest['name'])
            class_path = module_path + "." + file_manifest['name'].split(".")[0]
            loaded_file = importlib.machinery.SourceFileLoader("module", os_path).load_module()

            for component_manifest in file_manifest['components']:
                component_manifest['file_path'] = class_path
                component_manifest['package'] = module.manifest['package']
                component_class = getattr(loaded_file, component_manifest['name'])
                module.add_component(ModuleComponent(component_manifest, component_class))


    def fill_components(self, module):
        self.propagate_scope(module, 'views')
        self.propagate_scope(module, 'languages')

    def propagate_scope(self, module, manifest_string):
        component_files = module.manifest['files']
        pointer = 0
        view_scope = None
        if manifest_string in module.manifest:
            view_scope = module.manifest[manifest_string]
        for file_manifest in component_files:

            inner_view_scope = []
            if manifest_string in file_manifest:
                inner_view_scope = file_manifest[manifest_string]
            elif view_scope is not None:
                inner_view_scope = view_scope

            for component_manifest in file_manifest['components']:
                if manifest_string not in component_manifest:
                    module.components[pointer].manifest[manifest_string] = inner_view_scope
                pointer += 1

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

    def load_package_module(self, package_name):
        manifest = self.load_package_manifest(package_name)

        module = Module(manifest)
        self.add_components(module)
        self.fill_components(module)
        return module