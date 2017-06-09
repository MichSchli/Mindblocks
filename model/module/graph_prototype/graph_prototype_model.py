from model.component.subgraph_component import SubgraphComponentModel
from model.identifiables.identifiable import Identifiable

class GraphPrototypeModel(Identifiable):

    graph_identifier = None
    canvas_identifier = None
    prototype_class = SubgraphComponentModel

    def get_unique_identifier(self):
        return "Subgraph:"+self.canvas_identifier + "," + self.graph_identifier

    def get_name(self):
        return self.graph_identifier

    def get_package(self):
        return "subgraph"

    def get_attributes(self):
        return {'graph':self.graph_identifier, 'canvas':self.canvas_identifier}