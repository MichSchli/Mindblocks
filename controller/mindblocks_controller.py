from controller.description_panel_controller.description_panel_listener import DescriptionPanelListener
from controller.description_panel_controller.description_panel_presenter import DescriptionPanelPresenter
from controller.menubar_controller.menubar_listener import MenubarListener
from controller.selection_controller.selection_presenter import SelectionPresenter
from controller.toolbox_controller.toolbox_listener import ToolboxListener
from controller.viewscreen_controller.viewscreen_listener import ViewscreenListener
from controller.viewscreen_controller.viewscreen_presenter import ViewscreenPresenter
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

        self.selection_presenter = SelectionPresenter(self.canvas_repository)
        self.view = view

        self.viewscreen_listener = ViewscreenListener(self.view, self.canvas_repository, self.component_repository, self.graph_repository, self.selection_presenter)
        self.viewscreen_presenter = ViewscreenPresenter(self.view, self.canvas_repository, self.selection_presenter)

        self.menubar_listener = MenubarListener(self.view.menubar, self.canvas_repository, self.selection_presenter)

        self.toolbox_listener = ToolboxListener(self.view.toolbox, self.selection_presenter)

        self.description_panel_presenter = DescriptionPanelPresenter(self.view.description_panel, self.selection_presenter)
        self.description_panel_listener = DescriptionPanelListener(self.view.description_panel, self.component_repository, self.socket_repository, self.selection_presenter)

    def execute_graph(self, graph):
        runner = GraphRunner()
        return runner.run(graph, {})

    def load_all_canvases_from_file(self):
        input_file = self.view.select_load_file()
        canvas_list = self.canvas_repository.load_canvases(input_file)
        for canvas in canvas_list:
            self.view.process_view_in_ui(canvas)

    def create_new_canvas(self):
        canvas = self.canvas_repository.create_canvas()
        return canvas

    def update_toolbox(self):
        specification = ModuleSpecification()
        basic_modules = self.module_repository.get_basic_modules(specification)
        canvas_modules = self.module_repository.get_canvas_modules()

        all_modules = basic_modules + canvas_modules
        self.view.display_modules(all_modules)
