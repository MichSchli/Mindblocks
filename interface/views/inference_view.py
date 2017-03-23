from interface.drawable_canvas import DrawableCanvas


class InferenceView(DrawableCanvas):

    def __init__(self, parent, module_manager):
        self.view_name = 'inference'
        DrawableCanvas.__init__(self, parent, module_manager)

