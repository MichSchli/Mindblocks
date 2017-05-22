class VertexModel:

    graph = None
    edges_in = None
    edges_out = None

    def __init__(self):
        self.edges_in = []
        self.edges_out = []

    def add_ingoing_edge(self, edge):
        self.edges_in.append(edge)

    def add_outgoing_edge(self, edge):
        self.edges_out.append(edge)

    def get_edges_out(self):
        return self.edges_out

    def get_edges_in(self):
        return self.edges_in

    def in_degree(self):
        return len(self.edges_in)

    def get_graph(self):
        return self.graph

    def set_graph(self, graph):
        self.graph = graph

    def all_in_edges_satisfied(self):
        for edge in self.edges_in:
            if not edge.is_satisfied():
                return False
        return True

    '''
    Logic for evaluation:
    '''

    def push_by_index(self, index, value):
        self.edges_out[index].push(value)

    def pull_by_index(self, index):
        return self.edges_in[index].pull()