from NEW.model.identifiables.identifiable import Identifiable
from graph.edge import Edge


class Graph(Identifiable):
    """
    Class representing a computational graph. The graph is a directed, tripartite tree, with vertices split into
    operations, input-links, and output-links.
    """

    vertices = None
    edges = None

    def __init__(self, vertex=None):
        if vertex is not None:
            self.vertices = [vertex]
        else:
            self.vertices = []

        Identifiable.__init__(self, name="graph")

        self.edges = []

    def add_edge(self, u, v):
        edge = Edge(u, v)
        edge.set_graph(self)
        self.edges.append(edge)
        u.add_edge_out(edge)
        v.add_edge_in(edge)

        return edge

    def add_vertex(self, v):
        self.vertices.append(v)


    def merge_and_link(self, u, v):
        if self == u.get_graph() and not self == v.get_graph():
            self.merge(v.get_graph())
        elif self == v.get_graph() and not self == u.get_graph():
            self.merge(u.get_graph())

        return self.add_edge(u,v)

    def merge(self, other):
        for vertex in other.get_vertices():
            vertex.set_graph(self)

        for edge in other.get_edges():
            edge.set_graph(self)

        self.vertices.extend(other.get_vertices())
        self.edges.extend(other.get_edges())

    def get_vertices(self):
        return self.vertices

    def get_vertex_by_name(self, name):
        for vertex in self.vertices:
            if vertex.get_unique_identifier() == name:
                return vertex
        return None

    def get_edges(self):
        return self.edges

    def get_inputs(self):
        inputs = []
        for vertex in self.topological_walk():
            inputs.extend(vertex.theano_inputs())
        return inputs

    def get_outputs(self):
        outputs = []
        for vertex in self.topological_walk():
            outputs.extend(vertex.theano_outputs())
        return outputs

    def topological_walk(self):
        S = [vertex for vertex in self.vertices if vertex.in_degree() == 0]

        while len(S) > 0:
            next_vertex = S.pop()

            # Propagate forward in the graph:
            for out_edge in next_vertex.get_edges_out():
                out_edge.mark_satisfied(True)
                if out_edge.get_destination().is_satisfied():
                    S.append(out_edge.get_destination())

            yield next_vertex

        # Prepare for next traversal:
        for vertex in self.vertices:
            for out_edge in vertex.get_edges_out():
                out_edge.mark_satisfied(False)
