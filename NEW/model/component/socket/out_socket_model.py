from NEW.model.component.socket.abstract_socket_model import AbstractSocketModel


class OutSocketModel(AbstractSocketModel):

    def edge_valid(self, other_socket):
        if not other_socket.get_socket_type() == "in":
            return False
        if other_socket.get_parent_component() == self.get_parent_component():
            return False
        return True

    def get_socket_type(self):
        return "out"

    def compile_theano(self):
        value = self.pull_by_index(0)

        for edge in self.get_edges_out():
            edge.push(value)

    def compile_python(self):
        value = self.pull_by_index(0)

        for edge in self.get_edges_out():
            edge.push(value)