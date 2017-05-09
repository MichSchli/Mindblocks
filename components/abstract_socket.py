from graph.vertex import Vertex
from interface.graphics.graphic import *
from components.abstract_ui_representation import *
from theano import tensor as T


class AbstractSocket(Vertex):

    def __init__(self, parent, description):
        self.description = description
        self.parent = parent

        Vertex.__init__(self, name=self.name)

    def get_unique_identifier(self):
        return self.parent.get_unique_identifier() + ':' + self.description['name']

    def is_socket(self):
        return True

    def calculate_position_from_parent(self, parent_position):
        # TODO this is shit
        link_radius = 6
        vector = np.array(self.description['position'])
        scaled_vector = link_radius * vector / np.linalg.norm(vector)
        position = parent_position + vector + scaled_vector
        return position[0], position[1]

    def get_position(self):
        parent_position = self.parent.get_position()
        return self.calculate_position_from_parent(parent_position)



class OutSocket(AbstractSocket):

    def compile_theano(self):
        value = self.pull_by_index(0)

        for edge in self.get_edges_out():
            edge.push(value, self.get_edges_in()[0].type)

    def compile_python(self):
        value = self.pull_by_index(0)

        for edge in self.get_edges_out():
            edge.push(value, self.get_edges_in()[0].type)


class InSocket(AbstractSocket):

    def compile_theano(self):
        if len(self.get_edges_in()) == 1:
            self.push_by_index(0, self.pull_by_index(0), self.get_edges_in()[0].type)
        else:
            values = [edge.pull() for edge in self.get_edges_in()]
            concatenated = T.concatenate(values, axis=-1)
            self.push_by_index(0, concatenated)

    def compile_python(self):
        if len(self.get_edges_in()) == 1:
            self.push_by_index(0, self.pull_by_index(0), self.get_edges_in()[0].type)
        else:
            values = [edge.pull() for edge in self.get_edges_in()]
            self.push_by_index(0, values)