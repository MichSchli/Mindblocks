from model.component.component_model import ComponentModel
from model.component.component_specification import ComponentSpecification
from model.graph.graph_model import GraphModel


class ViewscreenListener:
    """
    Receives requests from viewscreen and enacts corresponding changes on model.
    """

    canvas_repository = None
    selection_presenter = None

    def __init__(self, viewscreen, canvas_repository, component_repository, graph_repository, selection_presenter):
        self.canvas_repository = canvas_repository
        self.selection_presenter = selection_presenter
        self.component_repository = component_repository
        self.graph_repository = graph_repository
        self.viewscreen = viewscreen

        self.register_observers()

    def register_observers(self):
        self.viewscreen.define_tab_changed_observer(self.tab_changed)
        self.viewscreen.define_click_observer(self.canvas_clicked)

    '''
    Events:
    '''

    def tab_changed(self, event):
        new_canvas_unique_identifier = event.new_canvas_unique_identifier
        new_canvas = self.canvas_repository.get_canvas_by_identifier(new_canvas_unique_identifier)
        self.selection_presenter.select_canvas(new_canvas)

    def canvas_clicked(self, event):
        selected_element = self.selection_presenter.selected_canvas_item.get()
        clicked_element = event.element
        toolbox_item = self.selection_presenter.selected_toolbox_item.get()

        if self.can_create_edge(selected_element, clicked_element):
            self.create_edge(selected_element, clicked_element)
        elif self.can_create_edge(clicked_element, selected_element):
            self.create_edge(clicked_element, selected_element)
        elif toolbox_item is not None:
            self.create_component_at(toolbox_item, event.location)
        else:
            self.selection_presenter.select_canvas_item(clicked_element)

    '''
    Helpers:
    '''

    def can_create_edge(self, element_1, element_2):
        if element_1 is None or element_2 is None:
            return False

        if not (element_1.is_socket() and element_2.is_socket()):
            return False

        return element_1.edge_valid(element_2)

    '''
    Actions:
    '''

    def create_component_at(self, toolbox_item, location):
        component = toolbox_item.prototype_class(None)
        component.prototype_id = toolbox_item.get_unique_identifier()
        component.set_position(location[0], location[1])
        component.update_attributes(toolbox_item.attributes)

        component = self.component_repository.create_component_with_sockets(component)

        canvas_model = self.selection_presenter.selected_canvas.get()

        graph_model = GraphModel(None)
        graph_model.add_component_with_sockets(component)
        graph_model.canvas_identifier = canvas_model.get_unique_identifier()

        graph_model = self.graph_repository.create(graph_model)

        canvas_model.defined_graphs.append(graph_model)
        self.canvas_repository.update_canvas(canvas_model)

        self.selection_presenter.select_canvas_item(component)

    def create_edge(self, out_socket, in_socket):
        target_socket_graph = in_socket.get_graph()
        self.graph_repository.unify_graphs(out_socket.get_graph(), in_socket.get_graph())
        self.graph_repository.add_edge_to_graph(out_socket.get_graph(), out_socket, in_socket)

        canvas_model = self.selection_presenter.selected_canvas.get()
        if target_socket_graph != out_socket.get_graph():
            canvas_model.delete_graph(target_socket_graph)

        self.canvas_repository.update_canvas(canvas_model)

