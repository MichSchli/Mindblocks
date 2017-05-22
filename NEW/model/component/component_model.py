from NEW.model.identifiables.identifiable import Identifiable
from NEW.model.graph.vertex_model import VertexModel


class ComponentModel(VertexModel, Identifiable):

    default_attributes = {}
    attributes = None

    default_in_sockets = []
    default_out_sockets = []
    source_string = None
    chosen_language = None
    position = None

    in_sockets = []
    out_sockets = []

    def __init__(self, identifier, module):
        self.module = module

        self.in_sockets = []
        self.out_sockets = []
        self.attributes = self.default_attributes

        VertexModel.__init__(self)
        Identifiable.__init__(self, unique_identifier=identifier)

    def get_default_in_sockets(self):
        return self.default_in_sockets

    def get_default_out_sockets(self):
        return self.default_out_sockets

    def parse_attributes(self):
        return True

    def get_attributes(self):
        return self.attributes

    def add_in_socket(self, socket):
        self.in_sockets.append(socket)

    def add_out_socket(self, socket):
        self.out_sockets.append(socket)

    def set_position(self, x, y):
        self.attributes['x'] = str(x)
        self.attributes['y'] = str(y)
        self.position = [x, y]

    def get_position(self):
        return self.position

    '''
    def update_attributes(self, new_attributes):
        for k,v in new_attributes.items():
            self.attributes[k] = v

        if 'x' in self.attributes and 'y' in new_attributes:
            x = int(self.attributes['x'])
            y = int(self.attributes['y'])

            self.set_position(x,y)



    def get_module_component(self):
        return self.module


    def create_sockets(self):
        self.in_sockets = []
        for description in self.default_in_sockets:
            link = InSocket(self, description)
            link.add_edge(self)
            self.in_sockets.append(link)

        self.out_sockets = []
        for description in self.default_out_sockets:
            link = OutSocket(self, description)
            self.add_edge(link)
            self.out_sockets.append(link)


    def get_out_socket_by_id(self, id):
        return self.get_edges_out()[id].destination

    def get_in_socket_by_id(self, id):
        return self.get_edges_in()[id].origin

    def get_out_socket_by_name(self, name):
        for edge in self.get_edges_out():
            if edge.destination.description['name'] == name:
                return edge.destination
        return None

    def get_in_socket_by_name(self, name):
        for edge in self.get_edges_in():
            if edge.origin.description['name'] == name:
                return edge.origin
        return None

    '''


