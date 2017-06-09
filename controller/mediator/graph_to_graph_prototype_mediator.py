from model.module.graph_prototype.graph_prototype_model import GraphPrototypeModel
from model.module.graph_prototype.graph_prototype_specifications import GraphPrototypeSpecifications


class GraphToGraphPrototypeMediator:

    def __init__(self, graph_repository, graph_prototype_repository):
        self.graph_repositoty = graph_repository
        self.graph_prototype_repository = graph_prototype_repository

        self.register_observers()

    def register_observers(self):
        self.graph_repositoty.define_create_observer(self.graph_created)
        self.graph_repositoty.define_update_observer(self.graph_updated)
        self.graph_repositoty.define_delete_observer(self.graph_deleted)

    '''
    Events:
    '''

    def graph_created(self, event):
        graph = event.element
        canvas_id = graph.get_canvas_identifier()

        self.create_subgraph_module(canvas_id, graph)

    def graph_updated(self, event):
        self.update_subgraph_module(event.element)

    def graph_deleted(self, event):
        self.delete_subgraph_module(event.element)

    '''
    Actions:
    '''

    def create_subgraph_module(self, canvas_id, graph):
        model = GraphPrototypeModel()
        model.canvas_identifier = canvas_id
        model.graph_identifier = graph.get_unique_identifier()
        self.graph_prototype_repository.create(model)

        print(graph.get_inputs())
        print(graph.get_outputs())

        #Manage sockets

    def update_subgraph_module(self, graph):
        pass

    def delete_subgraph_module(self, graph):
        specifications = GraphPrototypeSpecifications()
        specifications.graph_identifier = graph.get_unique_identifier()
        self.graph_prototype_repository.delete(specifications)
