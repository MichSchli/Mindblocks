class DescriptionPanelPresenter:
    """
    Listens for changes in model and updates the description panel to reflect those changes.
    """

    def __init__(self, description_panel, selection_presenter):
        self.selection_presenter = selection_presenter
        self.description_panel = description_panel

        self.register_observers()

    def register_observers(self):
        self.selection_presenter.selected_canvas_item.define_observer(self.element_selection_changed, event='selection_changed')

    '''
    Listeners:
    '''

    def element_selection_changed(self, event):
        print("haha")

    '''
    Actions:
    '''

    def clear_description_panel(self):
        pass

    def 