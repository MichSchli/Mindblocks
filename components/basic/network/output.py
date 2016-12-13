import imp

abstract = imp.load_source('abstract', 'components/component.py')

class Output(abstract.Component):

    name = "Output"
    links_in = [{'position': [0,20],
                 'name': 'Input'}]

    def copy(self, identifier=None):
        return Output(identifier=identifier)

    def theano_outputs(self):
        return [self.pull_by_index(0)]


