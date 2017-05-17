class AbstractVertex:

    graph = None

    def get_graph(self):
        return self.graph

    def set_graph(self, graph):
        self.graph = graph