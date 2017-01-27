import theano.tensor as T

from components.component import Component


class Dot(Component):
    name = "DotProduct"
    links_out = [{'position': [0, -20],
                  'name': 'Output'}]
    links_in = [{'position': [-15, 20], 'name': 'Left'},
                {'position': [15, 20], 'name': 'Right'}]

    def compile_theano(self):
        left = self.pull_by_index(0)
        right = self.pull_by_index(1)
        self.push_by_index(0, T.dot(left, right))

    def copy(self, identifier=None):
        return Dot(identifier=identifier)
