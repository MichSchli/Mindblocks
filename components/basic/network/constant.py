import imp

import theano

from components.component import Component


class Constant(Component):
    name = "Constant"
    links_out = [{'position': [0, -20],
                  'name': 'Output'}]

    attributes = {'value':0}

    def compile_theano(self):
        self.push_by_index(0, theano.tensor.constant(self.attributes['value']))

    def copy(self, identifier=None):
        return Constant(identifier=identifier)
