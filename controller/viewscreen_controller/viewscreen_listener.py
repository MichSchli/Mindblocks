

class ViewscreenListener:
    """
    Receives requests from viewscreen and enacts corresponding changes on model.
    """

    canvas_repository = None
    selection_presenter = None

    def __init__(self, viewscreen, canvas_repository, selection_presenter):
        self.canvas_repository = canvas_repository
        self.selection_presenter = selection_presenter
        self.viewscreen = viewscreen

        self.register_observers()

    def register_observers(self):
        self.viewscreen.register_tab_changed_event_handler(self.tab_changed)

    '''
    Events:
    '''

    def tab_changed(self, new_canvas_unique_identifier):
        new_canvas = self.canvas_repository.get_canvas_by_identifier(new_canvas_unique_identifier)
        self.selection_presenter.select_canvas(new_canvas)
