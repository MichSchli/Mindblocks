from NEW.model.identifiables.identifiable import Identifiable


class EdgeModel(Identifiable):

    origin = None
    destination = None
    graph = None

    satisfied = False
    value = None

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def get_graph(self):
        return self.graph

    def set_graph(self, graph):
        self.graph = graph

    def get_unique_identifier(self):
        return self.origin.get_unique_identifier() + " -> " + self.destination.get_unique_identifier()

    def mark_satisfied(self, value):
        self.satisfied = value

    def is_satisfied(self):
        return self.satisfied

    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination

    '''
    Logic for evaluation:
    '''

    def push(self, value):
        self.value = value

    def pull(self):
        return self.value