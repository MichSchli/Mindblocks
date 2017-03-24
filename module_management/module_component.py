from components.graph.subgraph_component import SubgraphComponent

class ModuleComponent:

    def __init__(self, manifest, component_class):
        self.manifest = manifest
        self.component_class = component_class
        self.component_class.module = manifest['file_path']

    def instantiate(self, identifier=None):
        return self.component_class(manifest=self.manifest, identifier=identifier)

    def get_name(self):
        return self.manifest['name']

    # TODO: Hack
    def get_unique_identifier(self):
        return self.get_name()

    def get_attributes(self):
        return self.component_class.attributes


class GraphModuleComponent(ModuleComponent):

    def __init__(self, manifest, graph):
        self.manifest = manifest
        self.component_class = SubgraphComponent
        self.component_class.module = manifest['file_path']
        self.graph = graph

    def instantiate(self, identifier=None):
        return SubgraphComponent(self.graph, manifest=self.manifest, identifier=identifier)