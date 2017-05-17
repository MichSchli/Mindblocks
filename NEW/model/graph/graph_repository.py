from NEW.model.graph.edge_model import EdgeModel
from NEW.model.graph.graph_model import GraphModel
from NEW.observer.observable_dictionary import ObservableDict


class GraphRepository:

    defined_graphs = None

    def __init__(self, identifier_factory):
        self.identifier_factory = identifier_factory
        self.defined_graphs = ObservableDict()

    def create_graph(self):
        identifier = self.identifier_factory.get_next_identifier(name_string='graph')
        graph = GraphModel(identifier)
        self.defined_graphs.append(graph)
        return graph

    def add_vertex_to_graph(self, graph, vertex):
        graph.append_vertex(vertex)
        vertex.set_graph(graph)

    def add_edge_to_graph(self, graph, origin, destination):
        edge = EdgeModel(origin, destination)
        graph.append_edge(edge)
        edge.set_graph(graph)
        return edge

    def unify_graphs(self, graph_1, graph_2):
        if graph_1 == graph_2:
            return True

        for vertex in graph_2.get_vertices():
            graph_1.append_vertex(vertex)
            vertex.set_graph(graph_1)

        for edge in graph_2.get_edges():
            graph_1.append_edge(edge)
            edge.set_graph(graph_1)

        self.defined_graphs.delete(graph_2)

