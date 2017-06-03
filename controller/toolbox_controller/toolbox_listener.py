

class ToolboxListener:
    """
    Receives requests from toolbox and enacts corresponding changes on model.
    """

    toolbox = None
    selection_presenter = None

    def __init__(self, toolbox, selection_presenter):
        self.selection_presenter = selection_presenter
        self.toolbox = toolbox

        self.register_observers()

    def register_observers(self):
        self.toolbox.define_click_observer(self.toolbox_item_clicked)

    '''
    Events:
    '''

    def toolbox_item_clicked(self, event):
        self.selection_presenter.select_toolbox_item(event.component)
