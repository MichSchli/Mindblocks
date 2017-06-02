class ViewscreenPresenter:
    """
    Listens for changes in model and updates the view to reflect those changes.
    """

    def __init__(self, viewscreen, canvas_repository, selection_presenter):
        self.selection_presenter = selection_presenter
        self.canvas_repository = canvas_repository
        self.viewscreen = viewscreen

        self.register_observers()

    def register_observers(self):
        self.selection_presenter.selected_canvas.set_observer(self.canvas_selection_changed)
        self.canvas_repository.defined_canvases.set_observer(self.canvas_repository_changed)

    def canvas_changed_in_repository(self, canvas):
        pass

    def canvas_selection_changed(self, canvas_selection):
        self.show_canvas_in_ui(canvas_selection.get())

    def canvas_repository_changed(self, defined_canvas_dict):
        self.update_ui(defined_canvas_dict.as_list())

    '''
    Actions:
    '''

    def show_canvas_in_ui(self, canvas):
        self.viewscreen.show_canvas(canvas)

    def update_ui(self, defined_canvas_list):
        self.viewscreen.update_following_list(defined_canvas_list)