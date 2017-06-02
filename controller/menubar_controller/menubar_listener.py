

class MenubarListener:
    """
    Receives requests from menu bar and enacts corresponding changes on model.
    """

    menubar = None
    selection_presenter = None

    def __init__(self, menubar, canvas_repository, selection_presenter):
        self.selection_presenter = selection_presenter
        self.canvas_repository = canvas_repository
        self.menubar = menubar

        self.register_observers()

    def register_observers(self):
        self.menubar.message.set_observer(self.add_view)

    '''
    Events:
    '''

    def add_view(self, message):
        if message.message != "Add view":
            return

        canvas = self.canvas_repository.create_canvas()
        self.selection_presenter.select_canvas(canvas)