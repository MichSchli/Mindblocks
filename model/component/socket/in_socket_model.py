import theano.tensor as T

from model.component.socket.abstract_socket_model import AbstractSocketModel


class InSocketModel(AbstractSocketModel):

    def edge_valid(self, other_socket):
        return False

    def get_socket_type(self):
        return "in"

    def compile_theano(self):
        if len(self.get_edges_in()) == 1:
            self.push_by_index(0, self.pull_by_index(0))
        else:
            values = [edge.pull() for edge in self.get_edges_in()]
            concatenated = T.concatenate(values, axis=-1)
            self.push_by_index(0, concatenated)

    def compile_python(self):
        if len(self.get_edges_in()) == 1:
            self.push_by_index(0, self.pull_by_index(0))
        else:
            values = [edge.pull() for edge in self.get_edges_in()]
            self.push_by_index(0, values)
