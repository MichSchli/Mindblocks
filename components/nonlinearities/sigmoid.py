import theano.tensor as T

from components.component import Component


class Sigmoid(Component):
    name = "Sigmoid"
    links_out = [{'position': [0, -20],
                  'name': 'Output'}]
    links_in = [{'position': [0, 20], 'name': 'Input'}]

    def compile_theano(self):
        input = self.pull_by_index(0)
        self.push_by_index(0, T.nnet.sigmoid(input))

    def copy(self, identifier=None):
        return Sigmoid(identifier=identifier)
