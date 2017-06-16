import json
import os

from model.component.component_specification import ComponentSpecification
from model.component.subgraph_component import SubgraphComponentModel
from model.module.module_model import ModuleModel
from model.module.toolbox_item.toolbox_item_model import ToolboxItemModel
from model.module.toolbox_item.toolbox_item_specifications import ToolboxItemSpecifications
from observables.observable_dictionary import ObservableDict
from packages.graph.subgraph_component import SubgraphComponent


class ModuleRepository:

    modules = None
    component_dir = '/home/michael/Projects/Mindblocks/packages'

    prototype_repository = None
    graph_prototype_repository = None

    def __init__(self, prototype_repository, graph_prototype_repository):
        self.prototype_repository = prototype_repository
        self.graph_prototype_repository = graph_prototype_repository
        self.modules = ObservableDict()

    def load_basic_modules(self):
        for package_name in self.get_all_package_names():
            module = self.load_basic_module_by_package_name(package_name)
            self.modules.append(module)

    def load_basic_module_by_package_name(self, package_name):
        manifest = self.load_package_manifest(package_name)
        module = ModuleModel(manifest['name'])

        prototypes = self.prototype_repository.load_prototypes(manifest)
        module.extend_prototypes(prototypes)

        return module

    def get_prototype_by_id(self, id):
        for module in self.get_basic_modules(None):
            for prototype in module.components:
                print(prototype.get_unique_identifier())
                print(id)
                if prototype.get_unique_identifier() == id:
                    print(prototype)
                    return prototype

        print("NOT FOUND")

        for module in self.get_canvas_modules(None):
            for prototype in module.components:
                if prototype.get_unique_identifier() == id:
                    return prototype

        return None

    def get_prototype(self, specifications):
        basic_prototype = self.prototype_repository.get(specifications)

        if basic_prototype is not None:
            return basic_prototype

        graph_prototype = self.graph_prototype_repository.get(specifications)
        return graph_prototype

    def get_basic_modules(self, specifications):
        return list(self.modules.elements.values())

    def get_canvas_modules(self, specifications):
        prototypes = self.graph_prototype_repository.get_all()
        modules = {}

        for prototype in prototypes:
            if prototype.canvas_identifier not in modules:
                modules[prototype.canvas_identifier] = ModuleModel(prototype.canvas_identifier)

            modules[prototype.canvas_identifier].components.append(prototype)

        return list(modules.values())

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