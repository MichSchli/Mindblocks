

class MenubarListener:
    """
    Receives requests from menu bar and enacts corresponding changes on model.
    """

    menubar = None
    canvas_repository = None

    def __init__(self, menubar, canvas_repository, selection_presenter):
        self.canvas_repository = canvas_repository
        self.selection_presenter = selection_presenter
        self.menubar = menubar

        self.register_observers()

    def register_observers(self):
        self.menubar.define_add_view_observer(self.add_view)
        self.menubar.define_save_selected_canvas_observer(self.save_selected_canvas)

    '''
    Events:
    '''

    def add_view(self, event):
        canvas = self.canvas_repository.create_canvas()

    def save_selected_canvas(self, event):
        canvas = self.selection_presenter.selected_canvas.get()
        output_file = event.save_file
        self.canvas_repository.save_canvas(canvas, output_file)