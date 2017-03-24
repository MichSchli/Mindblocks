from interface.drawable_canvas import DrawableCanvas


class ExperimentView(DrawableCanvas):

    def __init__(self, parent, module_manager, identifier_factory):
        self.view_name = 'experiment'
        DrawableCanvas.__init__(self, parent, module_manager, identifier_factory)
