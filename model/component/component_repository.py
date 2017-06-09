from model.component.component_specification import ComponentSpecification
from model.component.socket.socket_specification import SocketSpecification
from model.component.subgraph_component import SubgraphComponentModel
from observables.observable_dictionary import ObservableDict


class ComponentRepository:

    defined_components = None

    def __init__(self, identifier_factory, socket_repository, module_repository, xml_helper):
        self.identifier_factory = identifier_factory
        self.socket_repository = socket_repository
        self.xml_helper = xml_helper
        self.module_repository = module_repository
        self.defined_components = ObservableDict()

    def create_component_with_sockets(self, specifications):
        if specifications.identifier is None:
            identifier = self.identifier_factory.get_next_identifier(name_string=specifications.module_name)
        else:
            identifier = specifications.identifier

        component_class = specifications.prototype_class
        component = component_class(identifier)

        component.module_name = specifications.module_name
        component.module_package = specifications.module_package

        component.update_attributes(specifications.attributes)

        if specifications.attributes is not None:
            component.update_attributes(specifications.attributes)

        if specifications.location is not None:
            component.set_position(specifications.location[0], specifications.location[1])

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

    def update_component(self, component):
        self.defined_components.update(component)

    def save_component(self, component, outfile):
        name = component.get_unique_identifier()
        print(self.xml_helper.get_header("component", {"name": name}, indentation=2), file=outfile)

        print(self.xml_helper.get_header("class", indentation=3) + component.module_name + self.xml_helper.get_footer("class"), file=outfile)
        print(self.xml_helper.get_header("package", indentation=3) + component.module_package + self.xml_helper.get_footer("package"), file=outfile)

        for attribute in component.attributes:
            print(self.xml_helper.get_header("attribute", {"key": attribute}, indentation=3)
                  + component.attributes[attribute] + self.xml_helper.get_footer("attribute"), file=outfile)

        for in_socket in component.get_in_sockets():
            out_socket_names = [e.origin.get_unique_identifier() for e in in_socket.get_edges_in()]
            if out_socket_names:
                in_socket_name = in_socket.description['name']
                socket_string = self.xml_helper.get_header("socket", {"name": in_socket_name}, indentation=3)
                socket_string += ",".join(out_socket_names)
                socket_string += self.xml_helper.get_footer("socket")
                print(socket_string, file=outfile)

        print(self.xml_helper.get_footer("component", indentation=2), file=outfile)

    def load_next_component(self, lines, start_index=0):
        symbol, attributes, next_index = self.xml_helper.pop_symbol(lines, start_index=start_index)
        name = attributes["name"]

        class_symbol = ""
        package_symbol = ""
        component_attributes = {}

        #TODO: This is a code smell
        edges = {}

        while symbol != "/component":
            symbol, attributes, next_index = self.xml_helper.pop_symbol(lines, start_index=next_index)
            if symbol == "class":
                class_symbol, _, next_index = self.xml_helper.pop_symbol(lines, start_index=next_index, expect_value=True)
            elif symbol == "package":
                package_symbol, _, next_index = self.xml_helper.pop_symbol(lines, start_index=next_index, expect_value=True)
            elif symbol == "attribute":
                value, _, next_index = self.xml_helper.pop_symbol(lines, start_index=next_index, expect_value=True)
                component_attributes[attributes['key']] = value
            elif symbol == "socket":
                target, _, next_index = self.xml_helper.pop_symbol(lines, start_index=next_index, expect_value=True)
                edges[attributes['name']] = target

        if not package_symbol == 'subgraph':
            module = self.module_repository.get_basic_module_by_package_name(package_symbol)
            module_component = module.get_prototype(class_symbol).prototype_class
        else:
            module_component = SubgraphComponentModel

        specifications = ComponentSpecification()
        specifications.module_name = class_symbol
        specifications.module_package = package_symbol
        specifications.prototype_class = module_component
        specifications.attributes = component_attributes
        specifications.identifier = name
        component = self.create_component_with_sockets(specifications)

        return component, next_index, edges

    def create_subgraph_component(self, graph_model):
        pass
