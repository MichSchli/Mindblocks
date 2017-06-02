import theano.tensor as T

from model.component.component_model import ComponentModel


class Sigmoid(ComponentModel):
    name = "Sigmoid"
    default_out_sockets = [{'position': [0, -20],
                  'name': 'Output'}]
    default_in_sockets = [{'position': [0, 20], 'name': 'Input'}]

    def compile_theano(self):
        input = self.pull_by_index(0)
        self.push_by_index(0, T.nnet.sigmoid(input))
