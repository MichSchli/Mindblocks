from NEW.model.canvas.canvas_model import CanvasModel
from NEW.model.component.socket.socket_specification import SocketSpecification
from NEW.observer.observable_dictionary import ObservableDict


class ComponentRepository:

    defined_components = None

    def __init__(self, identifier_factory, socket_repository, xml_helper):
        self.identifier_factory = identifier_factory
        self.socket_repository = socket_repository
        self.xml_helper = xml_helper
        self.defined_components = ObservableDict()

    def create_component_with_sockets(self, specifications):
        if specifications.identifier is None:
            identifier = self.identifier_factory.get_next_identifier(name_string=specifications.module_component.get_name())

        component_class = specifications.module_component.prototype_class
        component = component_class(identifier, specifications.module_component)

        for in_socket_description in component.get_default_in_sockets():
            socket_specification = SocketSpecification()
            socket_specification.parent_component = component
            socket_specification.socket_type = "in"
            socket_specification.description = in_socket_description
            component.add_in_socket(self.socket_repository.create_socket(socket_specification))

        for out_socket_description in component.get_default_out_sockets():
            socket_specification = SocketSpecification()
            socket_specification.parent_component = component
            socket_specification.socket_type = "out"
            socket_specification.description = out_socket_description
            component.add_out_socket(self.socket_repository.create_socket(socket_specification))

        self.defined_components.append(component)
        return component

    def save_component(self, component, outfile):
        name = component.get_unique_identifier()
        print(self.xml_helper.get_header("component", {"name": name}, indentation=2), file=outfile)

        print(self.xml_helper.get_header("class", indentation=3) + component.module.manifest['name'] + self.xml_helper.get_footer("class"), file=outfile)
        print(self.xml_helper.get_header("package", indentation=3) + component.module.manifest['package'] + self.xml_helper.get_footer("package"), file=outfile)

        for attribute in component.attributes:
            print(self.xml_helper.get_header("attribute", {"key": attribute}, indentation=3)
                  + component.attributes[attribute] + self.xml_helper.get_footer("attribute"), file=outfile)

        #for edge in vertex.get_edges_in():
        #    in_socket = edge.get_origin()
        #    if in_socket.is_socket():
        #        out_socket_names = [e.origin.get_unique_identifier() for e in in_socket.get_edges_in()]
        #        if out_socket_names:
        #            in_socket_name = in_socket.description['name']
        #            socket_string = self.get_header("socket", {"name": in_socket_name}, indentation=3)
        #            socket_string += ",".join(out_socket_names)
        #            socket_string += self.get_footer("socket")
        #            yield socket_string

        print(self.xml_helper.get_footer("component", indentation=2), file=outfile)
