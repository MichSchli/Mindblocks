from model.graph.edge_model import EdgeModel

from model.identifiables.identifiable import Identifiable


class GraphModel(Identifiable):

    vertices = None
    edges = None
    canvas_identifier = None

    def __init__(self, unique_identifier):
        self.vertices = []
        self.edges = []
        Identifiable.__init__(self, unique_identifier=unique_identifier)

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_canvas_identifier(self):
        return self.canvas_identifier

    def get_vertex_by_name(self, identifier):
        for vertex in self.vertices:
            if vertex.get_unique_identifier() == identifier:
                return vertex
        return None

    def append_vertex(self, vertex):
        self.vertices.append(vertex)

    def append_edge(self, edge):
        self.edges.append(edge)

    def add_vertex(self, vertex):
        self.append_vertex(vertex)
        vertex.set_graph(self)

    def add_edge(self, origin, destination):
        edge = EdgeModel(origin, destination)
        self.append_edge(edge)
        edge.set_graph(self)

        origin.add_outgoing_edge(edge)
        destination.add_ingoing_edge(edge)
        return edge

    def add_component_with_sockets(self, component):
        self.add_vertex(component)
        component.set_graph(self)

        for out_socket in component.get_out_sockets():
            self.add_vertex(out_socket)
            self.add_edge(component, out_socket)

        for in_socket in component.get_in_sockets():
            self.add_vertex(in_socket)
            self.add_edge(in_socket, component)

    def topological_walk(self, components_only=False):
        S = [vertex for vertex in self.vertices if vertex.in_degree() == 0]

        while len(S) > 0:
            next_vertex = S.pop()

            # Propagate forward in the graph:
            for out_edge in next_vertex.get_edges_out():
                out_edge.mark_satisfied(True)
                if out_edge.get_destination().all_in_edges_satisfied():
                    S.append(out_edge.get_destination())

            if not (components_only and next_vertex.is_socket()):
                yield next_vertex

        # Prepare for next traversal:
        for vertex in self.vertices:
            for out_edge in vertex.get_edges_out():
                out_edge.mark_satisfied(False)

    def get_inputs(self):
        inputs = []
        for component in self.topological_walk(components_only=True):
            inputs.extend(component.get_theano_inputs())

        return inputs

    def get_outputs(self):
        outputs = []
        for component in self.topological_walk(components_only=True):
            outputs.extend(component.get_theano_outputs())

        return outputs