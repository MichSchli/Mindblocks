import imp

abstract = imp.load_source('abstract', 'components/component.py')
graphic = imp.load_source('graphic', 'interface/graphics/graphic.py')

class Constant(abstract.Component):

    name = "Constant"
    value = 0

    def compile_theano(self):
        self.links_out[0].set_value(theano.tensor.constant(self.value))

    def copy(self, identifier=None):
        return Constant(identifier=identifier)

    def get_links_out(self):
        return [{'position': [0,-20],
                 'name': 'Output'}]

