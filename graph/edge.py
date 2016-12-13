class Edge:

    value = None

    def __init__(self, u, v):
        self.satisfied = False
        self.origin = u
        self.destination = v

    def set_graph(self, graph):
        self.graph = graph

    def mark_satisfied(self, value):
        self.satisfied = value

    def get_destination(self):
        return self.destination

    def push(self, value):
        self.value = value

    def pull(self):
        return self.value