from graph.graph import Graph
from identifiables.identifiable import Identifiable

class Vertex(Identifiable):
    graph = None
    attributes = None
    manifest = None

    def is_socket(self):
        return False

    def __init__(self, name="vertex"):
        Identifiable.__init__(self, name=name)
        self.edges_out = []
        self.edges_in = []
        self.initialize_graph()
        self.attributes = {}

    def get_attributes(self):
        return self.attributes

    def parse_attributes(self):
        return True

    def get_upstream_trainables(self):
        trainables = []
        for edge in self.edges_in:
            vertex = edge.origin
            trainables.extend(vertex.get_upstream_trainables())
        return trainables

    def get_name(self):
        return self.name

    def push_by_index(self, index, value, type='tensor'):
        self.edges_out[index].push(value, type)

    def pull_by_index(self, index):
        return self.edges_in[index].pull()

    def set_graph(self, graph):
        self.graph = graph

    def initialize_graph(self):
        self.set_graph(Graph(self))

    def add_edge(self, other):
        return self.graph.merge_and_link(self, other)

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

    def theano_updates(self):
        return []

    def compile_theano(self):
        pass

    def compile_python(self):
        pass