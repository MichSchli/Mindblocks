import imp

abstract = imp.load_source('abstract', 'components/component.py')

class Output(abstract.Component):

    name = "Output"
    links_in = [{'position': [0,20],
                 'name': 'Input'}]

    def copy(self, identifier=None):
        return Output(identifier=identifier)

    def theano_outputs(self):
        to_be_output = self.pull_by_index(0)

        print(self.edges_in[0].type)

        if self.edges_in[0].type == 'scalar' or self.edges_in[0].type == 'tensor':
            return [to_be_output]
        elif self.edges_in[0].type == 'list':
            return to_be_output


