from identifiables.identifiable import Identifiable


class View(Identifiable):

    name = None

    defined_graphs = None
    module_manager = None
    identifier_factory = None

    def __init__(self, name, identifier_factory):
        self.name = name

        self.defined_graphs = []

        self.identifier_factory = identifier_factory

    def load_modules(self):
        modules = self.module_manager.fetch_basic_modules(view=self.name)
        modules.extend(self.module_manager.fetch_graph_modules(view=self.name))
        self.available_modules = modules

    def get_available_modules(self):
        return self.available_modules

    def get_defined_graphs(self):
        return self.defined_graphs

    def append_graph(self, graph):
        self.defined_graphs.append(graph)

    def remove_graph(self, graph):
        self.defined_graphs.remove(graph)
        self.module_manager.delete_graph(self.name, graph)

    def instantiate(self, module_component):
        component = module_component.instantiate()
        component.create_sockets()
        self.identifier_factory.assign_identifier(component)
        self.identifier_factory.assign_identifier(component.get_graph())
        self.append_graph(component.get_graph())
        return component

    def create_edge(self, out_vertex, in_vertex):
        if out_vertex.get_graph() != in_vertex.get_graph():
            self.remove_graph(in_vertex.get_graph())

        out_vertex.add_edge(in_vertex)