from NEW.model.component.socket.abstract_socket_model import AbstractSocketModel
import theano.tensor as T

class InSocketModel(AbstractSocketModel):

    def edge_valid(self, other_socket):
        if not other_socket.get_socket_type() == "out":
            return False
        if other_socket.get_parent_component() == self.get_parent_component():
            return False
        return True

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
