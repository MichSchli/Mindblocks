from graph.edge import Edge
from identifiables.identifiable import Identifiable


class GraphModel(Identifiable):

    vertices = None
    edges = None

    def __init__(self, unique_identifier):
        self.vertices = []
        self.edges = []
        Identifiable.__init__(self, unique_identifier=unique_identifier)

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def append_vertex(self, vertex):
        self.vertices.append(vertex)

    def append_edge(self, edge):
        self.edges.append(edge)