from model.canvas.canvas_repository import CanvasRepository
from model.component.component_repository import ComponentRepository
from model.component.component_specification import ComponentSpecification
from model.component.socket.socket_repository import SocketRepository
from model.graph.graph_repository import GraphRepository
from model.graph.graph_runners.python_graph_runner import GraphRunner
from model.identifiables.identifier_factory import IdentifierFactory
from model.module.module_specification import ModuleSpecification
from model.module.toolbox_item.toolbox_item_repository import ToolboxItemRepository

from helpers.xml.xml_helper import XmlHelper
from model.module.module_repository import ModuleRepository


class MindblocksController:

    canvas_repository = None
    view = None

    def __init__(self, view):
        self.identifier_factory = IdentifierFactory()
        self.xml_helper = XmlHelper()

        self.prototype_repository = ToolboxItemRepository()
        self.module_repository = ModuleRepository(self.prototype_repository)

        self.socket_repository = SocketRepository(self.identifier_factory)
        self.component_repository = ComponentRepository(self.identifier_factory, self.socket_repository, self.module_repository, self.xml_helper)

        self.graph_repository = GraphRepository(self.identifier_factory, self.component_repository, self.xml_helper)
        self.canvas_repository = CanvasRepository(self.identifier_factory, self.graph_repository, self.xml_helper)


        self.view = view

    def execute_graph(self, graph):
        runner = GraphRunner()
        return runner.run(graph, {})

    def save_single_canvas(self, canvas):
        output_file = self.view.select_save_file()
        self.canvas_repository.save_canvas(canvas, output_file)

    def load_all_canvases_from_file(self):
        input_file = self.view.select_load_file()
        canvas_list = self.canvas_repository.load_canvases(input_file)
        for canvas in canvas_list:
            self.view.process_view_in_ui(canvas)

    def create_new_canvas(self):
        canvas = self.canvas_repository.create_canvas()
        self.view.process_view_in_ui(canvas)
        return canvas

    def update_toolbox(self):
        specification = ModuleSpecification()
        basic_modules = self.module_repository.get_basic_modules(specification)
        canvas_modules = self.module_repository.get_canvas_modules()

        all_modules = basic_modules + canvas_modules
        self.view.display_modules(all_modules)

    def create_component_with_sockets(self, module_component, canvas_model, location):
        specifications = ComponentSpecification()
        specifications.module_component = module_component

        component = self.component_repository.create_component_with_sockets(specifications)

        graph_model = self.graph_repository.create_graph()
        graph_model.add_component_with_sockets(component)
        self.graph_repository.update_graph(graph_model)

        canvas_model.defined_graphs.append(graph_model)
        self.canvas_repository.update_canvas(canvas_model)

        self.view.process_component_in_ui(component, location)
        return component

    def create_edge(self, socket_1, socket_2):
        if not socket_1.edge_valid(socket_2):
            return None

        self.graph_repository.unify_graphs(socket_1.get_graph(), socket_2.get_graph())

        edge = self.graph_repository.add_edge_to_graph(socket_1.get_graph(), socket_1, socket_2)

        self.view.process_edge_in_ui(edge)
        return edge