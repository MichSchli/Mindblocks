from NEW.model.identifiables.identifiable import Identifiable


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

    def topological_walk(self):
        S = [vertex for vertex in self.vertices if vertex.in_degree() == 0]

        while len(S) > 0:
            next_vertex = S.pop()

            # Propagate forward in the graph:
            for out_edge in next_vertex.get_edges_out():
                out_edge.mark_satisfied(True)
                if out_edge.get_destination().all_in_edges_satisfied():
                    S.append(out_edge.get_destination())

            yield next_vertex

        # Prepare for next traversal:
        for vertex in self.vertices:
            for out_edge in vertex.get_edges_out():
                out_edge.mark_satisfied(False)