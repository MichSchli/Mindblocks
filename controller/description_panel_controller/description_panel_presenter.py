from controller.description_panel_controller.description_view_model import DescriptionViewModel


class DescriptionPanelPresenter:
    """
    Listens for changes in model and updates the description panel to reflect those changes.
    """

    def __init__(self, description_panel, selection_presenter):
        self.selection_presenter = selection_presenter
        self.description_panel = description_panel

        self.register_observers()

    def register_observers(self):
        self.selection_presenter.selected_canvas_item.define_observer(self.selection_changed, event='selection_changed')
        self.selection_presenter.selected_toolbox_item.define_observer(self.selection_changed, event='selection_changed')

    '''
    Listeners:
    '''

    def selection_changed(self, event):
        self.update_description_panel()

    '''
    Actions:
    '''

    def update_description_panel(self):
        description_view_model = DescriptionViewModel()

        canvas_item = self.selection_presenter.selected_canvas_item.get()
        toolbox_item = self.selection_presenter.selected_toolbox_item.get()

        if canvas_item is not None:
            self.decorate_view_model_from_canvas_item(description_view_model, canvas_item)
        elif toolbox_item is not None:
            self.decorate_view_model_from_toolbox_item(description_view_model, toolbox_item)

        self.description_panel.update_from_view_model(description_view_model)

    '''
    Helpers:
    '''

    def decorate_view_model_from_canvas_item(self, description_view_model, canvas_item):
        description_view_model.title = canvas_item.get_unique_identifier()

        for k,v in canvas_item.get_attributes().items():
            if k == 'x' or k == 'y':
                continue
            description_view_model.text_attributes[k] = v


    def decorate_view_model_from_toolbox_item(self, description_view_model, toolbox_item):
        description_view_model.title = toolbox_item.get_name()

        for k,v in toolbox_item.get_attributes().items():
            description_view_model.text_attributes[k] = v
