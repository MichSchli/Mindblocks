class Edge:

    value = None
    type=None
    graph=None
    attributes = None

    def __init__(self, u, v):
        self.satisfied = False
        self.origin = u
        self.destination = v
        self.attributes = {}

    def set_graph(self, graph):
        self.graph = graph

    def get_graph(self):
        return self.graph

    def mark_satisfied(self, value):
        self.satisfied = value

    def get_destination(self):
        return self.destination

    def get_origin(self):
        return self.origin

    def push(self, value, type=None):
        self.type = type
        self.value = value

    def pull(self):
        return self.value


    def get_in_socket_name(self):
        if 'in_socket' in self.attributes:
            return self.attributes['in_socket']
        return "ERROR"

    def get_out_socket_name(self):
        if 'out_socket' in self.attributes:
            return self.attributes['out_socket']
        return "ERROR"