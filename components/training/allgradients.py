import theano.tensor as T

from components.component import Component


class AllGradients(Component):
    name = "AllGradients"
    links_out = [{'position': [0, -20],
                  'name': 'Output'}
                 ]
    links_in = [{'position': [0, 20],
                 'name': 'Function'}]

    def compile_theano(self):
        trainables = self.get_upstream_trainables()
        function = self.pull_by_index(0)
        print(trainables)
        print(function)
        self.push_by_index(0, T.grad(function, wrt=trainables), type='list')
