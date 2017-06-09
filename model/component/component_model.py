from model.graph.vertex_model import VertexModel

from model.identifiables.identifiable import Identifiable


class ComponentModel(VertexModel, Identifiable):

    default_attributes = {}
    attributes = None

    default_in_sockets = []
    default_out_sockets = []
    source_string = None
    chosen_language = None
    position = None

    module_name = None
    module_package = None

    in_sockets = []
    out_sockets = []

    def __init__(self, identifier):

        self.in_sockets = []
        self.out_sockets = []
        self.attributes = {}

        VertexModel.__init__(self)
        Identifiable.__init__(self, unique_identifier=identifier)

    def is_socket(self):
        return False

    def get_default_in_sockets(self):
        return self.default_in_sockets

    def get_default_out_sockets(self):
        return self.default_out_sockets

    def get_out_sockets(self):
        return self.out_sockets

    def get_in_sockets(self):
        return self.in_sockets

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

    def update_attributes(self, new_attributes):
        for k,v in new_attributes.items():
            self.attributes[k] = v

        if 'x' in self.attributes and 'y' in new_attributes:
            x = int(self.attributes['x'])
            y = int(self.attributes['y'])

            self.set_position(x,y)

    def get_out_socket_by_name(self, name):
        for socket in self.get_out_sockets():
            if socket.description['name'] == name:
                return socket
        return None

    def get_in_socket_by_name(self, name):
        for socket in self.get_in_sockets():
            if socket.description['name'] == name:
                return socket
        return None

    def get_theano_inputs(self):
        return []

    def get_theano_outputs(self):
        return []

