import imp

abstract = imp.load_source('abstract', 'components/component.py')

class Output(abstract.Component):

    name = "Output"

    def copy(self, identifier=None):
        return Output(identifier=identifier)

    def outputs(self):
        return [self.links_in[0].get_value()]

    def get_links_in(self):
        return [{'position': [0,20],
                 'name': 'Input'}]


