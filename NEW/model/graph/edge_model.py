from identifiables.identifiable import Identifiable


class EdgeModel(Identifiable):

    origin = None
    destination = None
    graph = None

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def get_graph(self):
        return self.graph

    def set_graph(self, graph):
        self.graph = graph

    def get_unique_identifier(self):
        return self.origin.get_unique_identifier() + " -> " + self.destination.get_unique_identifier()