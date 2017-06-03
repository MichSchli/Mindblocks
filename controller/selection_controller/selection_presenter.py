from observables.selection import Selection


class SelectionPresenter:

    selected_canvas = None
    selected_canvas_item = None
    selected_toolbox_item = None

    canvas_repository = None

    def __init__(self, canvas_repository):
        self.selected_canvas = Selection(None)
        self.selected_canvas_item = Selection(None)
        self.selected_toolbox_item = Selection(None)
        self.canvas_repository = canvas_repository

    '''
    Actions:
    '''

    def select_toolbox_item(self, toolbox_item):
        self.selected_toolbox_item.change(toolbox_item)
        self.selected_canvas_item.change(None)

    def select_canvas_item(self, canvas_item):
        self.selected_toolbox_item.change(None)
        self.selected_canvas_item.change(canvas_item)

    def select_canvas(self, canvas):
        self.selected_canvas.change(canvas)
        self.selected_canvas_item.change(None)

    def clear_selection(self):
        self.selected_toolbox_item.change(None)
        self.selected_canvas_item.change(None)