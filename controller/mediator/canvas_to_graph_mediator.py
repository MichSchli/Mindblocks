class CanvasToGraphMediator:
    """
    Listens for changes in views and updates graphs accordingly.
    """

    def __init__(self, canvas_repository, graph_repository):
        self.graph_repositoty = graph_repository
        self.canvas_repository = canvas_repository

        self.register_observers()

    def register_observers(self):
        self.canvas_repository.define_create_observer(self.canvas_created)

    '''
    Events:
    '''

    def canvas_created(self, event):
        canvas = event.element
        graphs = canvas.get_graphs()

        self.create_graphs(graphs)

    '''
    Actions:
    '''

    def create_graphs(self, graphs):
        for graph in graphs:
            self.graph_repositoty.create(graph)