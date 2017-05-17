from NEW.model.component.socket.abstract_socket_model import AbstractSocketModel


class InSocketModel(AbstractSocketModel):

    def edge_valid(self, other_socket):
        if not other_socket.get_socket_type() == "out":
            return False
        if other_socket.get_parent_component() == self.get_parent_component():
            return False
        return True

    def get_socket_type(self):
        return "in"
