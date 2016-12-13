import imp

import theano

abstract = imp.load_source('abstract', 'components/component.py')
graphic = imp.load_source('graphic', 'interface/graphics/graphic.py')


class Constant(abstract.Component):
    name = "Constant"
    value = [2,3]
    links_out = [{'position': [0, -20],
                  'name': 'Output'}]

    def compile_theano(self):
        self.push_by_index(0, theano.tensor.constant(self.value))

    def copy(self, identifier=None):
        return Constant(identifier=identifier)
