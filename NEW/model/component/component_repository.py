from NEW.model.canvas.canvas_model import CanvasModel
from NEW.model.component.socket.socket_specification import SocketSpecification
from NEW.observer.observable_dictionary import ObservableDict


class ComponentRepository:

    defined_components = None

    def __init__(self, identifier_factory, socket_repository, graph_repository):
        self.identifier_factory = identifier_factory
        self.socket_repository = socket_repository
        self.graph_repository = graph_repository
        self.defined_components = ObservableDict()

    def create_component_with_sockets(self, specifications):
        if specifications.identifier is None:
            identifier = self.identifier_factory.get_next_identifier(name_string=specifications.module_component.get_name())

        component_class = specifications.module_component.prototype_class
        component = component_class(identifier, specifications.module)

        if specifications.graph is not None:
            self.graph_repository.add_vertex_to_graph(specifications.graph, component)

        for in_socket_description in component.get_default_in_sockets():
            socket_specification = SocketSpecification()
            socket_specification.graph = specifications.graph
            socket_specification.parent_component = component
            socket_specification.socket_type = "in"
            socket_specification.description = in_socket_description
            component.add_in_socket(self.socket_repository.create_socket(socket_specification))

        for out_socket_description in component.get_default_out_sockets():
            socket_specification = SocketSpecification()
            socket_specification.graph = specifications.graph
            socket_specification.parent_component = component
            socket_specification.socket_type = "out"
            socket_specification.description = out_socket_description
            component.add_out_socket(self.socket_repository.create_socket(socket_specification))

        self.defined_components.append(component)
        return component
