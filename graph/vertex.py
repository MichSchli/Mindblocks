from graph.graph import Graph


class Vertex:
    graph = None
    attributes = {}

    def __init__(self):
        self.edges_out = []
        self.edges_in = []
        self.initialize_graph()

    def push_by_index(self, index, value):
        self.edges_out[index].push(value)

    def pull_by_index(self, index):
        return self.edges_in[index].pull()

    def set_graph(self, graph):
        self.graph = graph

    def initialize_graph(self):
        self.set_graph(Graph(self))

    def add_edge(self, other):
        self.graph.merge_and_link(self, other)

    def get_graph(self):
        return self.graph

    def add_edge_out(self, edge):
        self.edges_out.append(edge)

    def add_edge_in(self, edge):
        self.edges_in.append(edge)

    def in_degree(self):
        return len(self.edges_in)

    def out_degree(self):
        return len(self.edges_out)

    def get_edges_out(self):
        return self.edges_out

    def get_edges_in(self):
        return self.edges_in

    def is_satisfied(self):
        for edge in self.edges_in:
            if edge.satisfied == False:
                return False
        return True

    def theano_inputs(self):
        return []

    def theano_outputs(self):
        return []

    def theano_parameters(self):
        return []

    def compile_theano(self):
        pass

class Operation(Vertex):
    def __init__(self):
        pass


class Link(Vertex):
    def __init__(self):
        pass

