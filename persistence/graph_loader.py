from graph.graph import Graph

class GraphLoader:

    def __init__(self, module_importer):
        self.module_importer = module_importer

    def load_next_graph(self, lines, start_index=0):
        symbol, attributes, next_index = self.pop_symbol(lines, start_index=start_index)
        name = attributes["name"]

        graph = Graph()
        graph.set_unique_identifier(name)

        symbol, attributes, _ = self.pop_symbol(lines, start_index=next_index)
        while symbol != "/graph":
            component, edges, next_index = self.load_next_component(lines, start_index=next_index)
            graph.merge(component.get_graph())

            for target_socket_name, source in edges.items():
                source = source.split(":")
                source_component = graph.get_vertex_by_name(source[0])
                source_socket_name = source[1]

                source_socket = source_component.get_out_socket_by_name(source_socket_name)
                target_socket = component.get_in_socket_by_name(target_socket_name)

                source_socket.add_edge(target_socket)


            symbol, attributes, _ = self.pop_symbol(lines, start_index=next_index)

        return graph

    def load_next_component(self, lines, start_index=0):
        symbol, attributes, next_index = self.pop_symbol(lines, start_index=start_index)
        name = attributes["name"]

        class_symbol = ""
        package_symbol = ""
        component_attributes = {}
        edges = {}

        while symbol != "/component":
            symbol, attributes, next_index = self.pop_symbol(lines, start_index=next_index)
            if symbol == "class":
                class_symbol, _, next_index = self.pop_symbol(lines, start_index=next_index, expect_value=True)
            elif symbol == "package":
                package_symbol, _, next_index = self.pop_symbol(lines, start_index=next_index, expect_value=True)
            elif symbol == "attribute":
                value, _, next_index = self.pop_symbol(lines, start_index=next_index, expect_value=True)
                component_attributes[attributes['key']] = value
            elif symbol == "socket":
                target, _, next_index = self.pop_symbol(lines, start_index=next_index, expect_value=True)
                edges[attributes['name']] = target


        module = self.module_importer.load_package_module(package_symbol)
        module_component = module.get_component(class_symbol)
        component = module_component.instantiate()

        for k,v in component_attributes.items():
            component.attributes[k] = v

        component.set_unique_identifier(name)

        return component, edges, next_index

    # Temporary
    def pop_symbol(self, lines, expect_value=False, start_index=0):
        scanner = start_index
        if expect_value:
            while lines[scanner] != "<":
                scanner += 1
            symbol = lines[start_index:scanner].strip()
            return symbol, [], scanner
        else:
            while lines[scanner] != ">":
                scanner += 1
            scanner += 1
            symbol = lines[start_index:scanner].strip()

        parts = symbol[1:-1].split(' ')

        name = parts[0]
        attributes = dict([tuple(att.split("=")) for att in parts[1:]])

        return name, attributes, scanner