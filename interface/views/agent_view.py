from interface.drawable_canvas import DrawableCanvas


class AgentView(DrawableCanvas):

    def __init__(self, parent, module_manager):
        self.view_name = 'agent'
        DrawableCanvas.__init__(self, parent, module_manager)
