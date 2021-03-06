from model.component.socket.in_socket_model import InSocketModel
from model.component.socket.out_socket_model import OutSocketModel
from observables.observable_dictionary import ObservableDict


class SocketRepository:

    defined_sockets = None

    def __init__(self, identifier_factory):
        self.identifier_factory = identifier_factory
        self.defined_sockets = ObservableDict()

    def create_socket(self, specification):
        socket_description = specification.description
        parent_component = specification.parent_component
        socket_type = specification.socket_type

        socket_identifier = socket_description['name']
        component_uid = parent_component.get_unique_identifier()
        socket_name = component_uid + ":" + socket_identifier

        socket_uid = socket_name

        if socket_type == "in":
            socket = InSocketModel(socket_uid)
        else:
            socket = OutSocketModel(socket_uid)

        socket.parent_component = parent_component
        socket.description = socket_description

        self.defined_sockets.append(socket)
        return socket

    def update_socket(self, socket):
        self.defined_sockets.update(socket)
