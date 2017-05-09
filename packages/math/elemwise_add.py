import theano.tensor as T

from components.abstract_component import Component


class Add(Component):
    name = "Addition"
    default_out_sockets = [{'position': [0, -20],
                  'name': 'Output'}]
    default_in_sockets = [{'position': [-15, 20], 'name': 'Left'},
                          {'position': [15, 20], 'name': 'Right'}]

    def compile_theano(self):
        left = self.pull_by_index(0)
        right = self.pull_by_index(1)
        self.push_by_index(0, left + right)

