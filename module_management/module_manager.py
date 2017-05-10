from module_management.module import Module
from module_management.module_component import GraphModuleComponent


class ModuleManager:

    basic_modules = []

    def __init__(self, importer):
        self.basic_modules = importer.import_modules()
        self.graphs = {}

    def fetch_basic_modules(self, view=None):
        modules = []
        for module in self.basic_modules:
            filtered_module = module.get_filtered_copy(view)
            if True: #filtered_module.has_components():
                modules.append(filtered_module)
        return modules

    def fetch_graph_modules(self, toolbox_view):
        graph_modules = []
        for view in self.graphs:
            if view != toolbox_view and self.graphs[view] != []:
                module = self.compile_graph_module(view)
                graph_modules.append(module)

        return graph_modules

    def compile_graph_module(self, target_view):
        module_manifest = {'name': target_view}
        module = Module(module_manifest)
        for graph in self.graphs[target_view]:
            manifest = {'file_path': 'components.graph.subgraph_component',
                        'name': 'SubgraphComponent',
                        'languages': ['python']}
            module.add_component(GraphModuleComponent(manifest, graph))

        return module

    def register_view(self, view):
        self.graphs[view.get_name()] = []

    def register_graph(self, view, graph):
        self.graphs[view].append(graph)

    def delete_graph(self, view, graph):
        print(graph.get_unique_identifier())
        new_graphs = []
        for stored_graph in self.graphs[view]:
            if stored_graph.get_unique_identifier() != graph.get_unique_identifier():
                new_graphs.append(stored_graph)
        self.graphs[view] = new_graphs