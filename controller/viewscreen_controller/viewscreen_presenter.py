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
        self.selection_presenter.selected_canvas.define_observer(self.canvas_selection_changed, event='selection_changed')
        self.canvas_repository.define_create_observer(self.canvas_created_in_repository)
        self.canvas_repository.define_update_observer(self.canvas_updated_in_repository)

    '''
    Listeners:
    '''

    def canvas_created_in_repository(self, event):
        self.add_canvas_to_ui(event.element)

    def canvas_updated_in_repository(self, event):
        self.redraw_canvas_in_ui(event.element)

    def canvas_selection_changed(self, event):
        self.show_canvas_in_ui(event.new_element)

    '''
    Actions:
    '''

    def add_canvas_to_ui(self, canvas):
        self.viewscreen.add_canvas(canvas)
        self.viewscreen.show_canvas(canvas)

    def show_canvas_in_ui(self, canvas):
        self.viewscreen.show_canvas(canvas)

    def redraw_canvas_in_ui(self, canvas):
        self.viewscreen.redraw_canvas(canvas)