

class DescriptionPanelListener:
    """
    Receives requests from description panel and enacts corresponding changes on model.
    """

    description_panel = None
    selection_presenter = None

    def __init__(self, description_panel, component_repository, socket_repository, selection_presenter):
        self.selection_presenter = selection_presenter
        self.description_panel = description_panel
        self.component_repository = component_repository
        self.socket_repository = socket_repository

        self.register_observers()

    def register_observers(self):
        self.description_panel.define_change_observer(self.description_panel_changed_view_model)

    '''
    Events:
    '''

    def description_panel_changed_view_model(self, event):
        canvas_item = self.selection_presenter.selected_canvas_item.get()

        if canvas_item is None:
            return

        updated_canvas_model = self.decorate_canvas_item_from_view_model(canvas_item, event.view_model)
        self.update_canvas_item_in_repository(updated_canvas_model)

    '''
    Helpers:
    '''

    def decorate_canvas_item_from_view_model(self, canvas_item, view_model):
        if not canvas_item.is_socket():
            canvas_item.update_attributes(view_model.text_attributes)

        return canvas_item

    '''
    Actions:
    '''

    def update_canvas_item_in_repository(self, updated_canvas_model):
        if updated_canvas_model.is_socket():
            self.socket_repository.update_socket(updated_canvas_model)
        else:
            self.component_repository.update_component(updated_canvas_model)
