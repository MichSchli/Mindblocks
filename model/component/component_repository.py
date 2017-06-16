from model.component.component_specification import ComponentSpecification
from model.component.socket.socket_specification import SocketSpecification
from model.component.subgraph_component import SubgraphComponentModel
from model.module.prototype_specifications import PrototypeSpecifications
from model.module.toolbox_item.toolbox_item_specifications import ToolboxItemSpecifications
from observables.observable_dictionary import ObservableDict


class ComponentRepository:

    defined_components = None

    def __init__(self, identifier_factory, socket_repository, module_repository, xml_helper):
        self.identifier_factory = identifier_factory
        self.socket_repository = socket_repository
        self.xml_helper = xml_helper
        self.module_repository = module_repository
        self.defined_components = ObservableDict()

    def create_component_with_sockets(self, component):
        prototype = self.module_repository.get_prototype_by_id(component.prototype_id)

        if component.get_unique_identifier() is None:
            identifier = self.identifier_factory.get_next_identifier(name_string=prototype.get_name())
            component.set_unique_identifier(identifier)

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

        toolbox_item_specification = PrototypeSpecifications()
        toolbox_item_specification.package = package_symbol
        toolbox_item_specification.name = class_symbol

        toolbox_item = self.module_repository.get_prototype(toolbox_item_specification)

        component = toolbox_item.prototype_class(None)
        component.prototype_id = toolbox_item.get_unique_identifier()
        component.update_attributes(toolbox_item.attributes)
        component.update_attributes(component_attributes)

        component = self.create_component_with_sockets(component)

        # TODO: Load all graphs, then load all components

        return component, next_index, edges