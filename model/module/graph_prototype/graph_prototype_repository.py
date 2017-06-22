from observables.observable_dictionary import ObservableDict


class GraphPrototypeRepository:

    defined_graph_prototypes = None

    def __init__(self):
        self.defined_graph_prototypes = ObservableDict()

    def create(self, graph_prototype):
        self.defined_graph_prototypes.append(graph_prototype)

    def update(self, graph_prototype):
        self.defined_graph_prototypes.update(graph_prototype)

    def delete(self, graph_prototype_specifications):
        graph_prototypes = self.get(graph_prototype_specifications)
        for graph_prototype in graph_prototypes:
            self.defined_graph_prototypes.delete(graph_prototype)

    def get(self, specifications):
        elements = []
        for prototype in self.defined_graph_prototypes.elements.values():
            if specifications.matches(prototype):
                elements.append(prototype)
        return elements

    def get_all(self):
        return self.defined_graph_prototypes.elements.values()