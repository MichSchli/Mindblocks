from packages.graph.subgraph_component import SubgraphComponent
from interface.graphics.graphic import PlaceholderGraphic

class ModuleComponent:

    def __init__(self, manifest, component_class):
        self.manifest = manifest
        self.component_class = component_class
        self.component_class.module = manifest['file_path']

    def instantiate(self, identifier=None):
        return self.component_class(manifest=self.manifest, identifier=identifier, module=self)

    def instantiate_graphic(self):
        if 'graphic' not in self.manifest:
            return PlaceholderGraphic(self.get_unique_identifier())

    def get_name(self):
        return self.manifest['name']

    # TODO: Hack
    def get_unique_identifier(self):
        return self.get_name()

    # TODO: HACK
    def get_default_in_sockets(self):
        return self.component_class.default_in_sockets

    def get_default_out_sockets(self):
        return self.component_class.default_out_sockets

    def get_attributes(self):
        return self.component_class.default_attributes


class GraphModuleComponent(ModuleComponent):

    def __init__(self, manifest, graph):
        self.manifest = manifest
        self.component_class = SubgraphComponent
        self.component_class.module = manifest['file_path']
        self.graph = graph

    def instantiate(self, identifier=None):
        sgc = SubgraphComponent(manifest=self.manifest, identifier=identifier)
        graph_attributes = {'target_view': 'abc', 'target_graph': self.graph.get_name()}
        sgc.update_attributes(graph_attributes)
        return sgc