from observables.selection import Selection


class ViewscreenController:
    """
    Defines controller-level logic for canvas objects:

    - Maintains canvas and object selector.
    - Provides point-of-contact for canvas-level interaction with user.
    - Listens for changes in canvas repository, updates view as required.

    """

    canvas_repository = None
    graph_repository = None

    selected_canvas = None

    def __init__(self, viewscreen, canvas_repository, graph_repository):
        self.canvas_repository = canvas_repository
        self.graph_repository = graph_repository
        self.viewscreen = viewscreen

        self.selected_canvas = Selection(None)

        self.register_observers()

    def register_observers(self):
        self.viewscreen.register_tab_changed_event_handler(self.tab_changed)

    '''
    Events:
    '''

    def canvas_clicked(self, location):
        pass

    def ui_element_clicked(self, ui_element):
        pass

    def tab_changed(self, new_canvas_unique_identifier):
        new_canvas = self.canvas_repository.get_canvas_by_identifier(new_canvas_unique_identifier)
        self.selected_canvas.change(new_canvas)

    def current_tab_clicked(self):
        pass

