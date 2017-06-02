from model.graph.graph_model import GraphModel
from observables.observable_dictionary import ObservableDict


class GraphRepository:

    defined_graphs = None
    xml_helper = None

    def __init__(self, identifier_factory, component_repository, xml_helper):
        self.identifier_factory = identifier_factory
        self.xml_helper = xml_helper
        self.component_repository = component_repository
        self.defined_graphs = ObservableDict()

    def create_graph(self):
        identifier = self.identifier_factory.get_next_identifier(name_string='graph')
        graph = GraphModel(identifier)
        self.defined_graphs.append(graph)
        return graph

    def add_vertex_to_graph(self, graph, vertex):
        graph.add_vertex(vertex)

    def add_edge_to_graph(self, graph, origin, destination):
        return graph.add_edge(origin, destination)

    def save_graph(self, graph, outfile):
        name = graph.get_unique_identifier()

        print(self.xml_helper.get_header("graph", {"name": name}, indentation=1), file=outfile)
        for component in graph.topological_walk(components_only=True):
            self.component_repository.save_component(component, outfile)
        print(self.xml_helper.get_footer("graph", indentation=1), file=outfile)

    def update_graph(self, graph):
        self.defined_graphs.update(graph)

    def load_next_graph(self, lines, start_index=0):
        symbol, attributes, next_index = self.xml_helper.pop_symbol(lines, start_index=start_index)
        name = attributes["name"]

        graph = GraphModel(name)

        symbol, attributes, _ = self.xml_helper.pop_symbol(lines, start_index=next_index)
        while symbol != "/graph":
            component, next_index, edges = self.component_repository.load_next_component(lines, start_index=next_index)
            graph.add_component_with_sockets(component)

            #TODO: This is a code smell
            for target_socket_name, source in edges.items():
                print(source)
                source = source.split(":")
                source_component = graph.get_vertex_by_name(source[0])
                source_socket_name = source[1]

                source_socket = source_component.get_out_socket_by_name(source_socket_name)
                target_socket = component.get_in_socket_by_name(target_socket_name)

                graph.add_edge(source_socket, target_socket)

            symbol, attributes, _ = self.xml_helper.pop_symbol(lines, start_index=next_index)

        self.update_graph(graph)

        symbol, attributes, next_index = self.xml_helper.pop_symbol(lines, start_index=next_index)
        return graph, next_index

    def unify_graphs(self, graph_1, graph_2):
        if graph_1 == graph_2:
            return True

        for vertex in graph_2.get_vertices():
            graph_1.append_vertex(vertex)
            vertex.set_graph(graph_1)

        for edge in graph_2.get_edges():
            graph_1.append_edge(edge)
            edge.set_graph(graph_1)

        self.defined_graphs.delete(graph_2)

