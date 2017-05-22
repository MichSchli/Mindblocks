import theano.tensor as T

from NEW.model.component.component_model import ComponentModel


class AllGradients(ComponentModel):
    name = "AllGradients"
    default_out_sockets = [{'position': [0, -20],
                  'name': 'Output'}
                           ]
    default_in_sockets = [{'position': [0, 20],
                 'name': 'Function'}]

    def compile_theano(self):
        trainables = self.get_upstream_trainables()
        function = self.pull_by_index(0)
        print(trainables)
        print(function)
        self.push_by_index(0, T.grad(function, wrt=trainables), type='list')
