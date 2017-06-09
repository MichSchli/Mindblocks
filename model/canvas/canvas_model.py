from model.identifiables.identifiable import Identifiable


class CanvasModel(Identifiable):

    defined_graphs = None

    def __init__(self, unique_identifier):
        self.defined_graphs = []
        Identifiable.__init__(self, unique_identifier=unique_identifier)

    def get_defined_graphs(self):
        return self.defined_graphs

    def append_graph(self, graph):
        self.defined_graphs.append(graph)

    def delete_graph(self, graph):
        for i,g in enumerate(self.defined_graphs):
            if g.get_unique_identifier() == graph.get_unique_identifier():
                del self.defined_graphs[i]
                break

    def get_graphs(self):
        return self.defined_graphs
