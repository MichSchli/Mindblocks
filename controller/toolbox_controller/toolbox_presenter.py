from model.module.module_specification import ModuleSpecification


class ToolboxPresenter:
    """
    Listens for changes in model and updates the description panel to reflect those changes.
    """

    def __init__(self, toolbox, module_repository, canvas_repository):
        self.toolbox = toolbox
        self.module_repository = module_repository
        self.canvas_repository = canvas_repository

        self.register_observers()

    def register_observers(self):
        self.canvas_repository.define_update_observer(self.update_toolbox)

    '''
    Actions:
    '''

    def update_toolbox(self, event):
        specification = ModuleSpecification()
        basic_modules = self.module_repository.get_basic_modules(specification)
        all_canvases = self.canvas_repository.get_all_canvases()

        canvas_modules = self.module_repository.get_canvas_modules(all_canvases)

        all_modules = basic_modules + canvas_modules
        self.toolbox.display_modules(all_modules)

