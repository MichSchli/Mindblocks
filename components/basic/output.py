from components.component import Component

class Output(Component):

    name = "Output"
    links_in = [{'position': [0,20],
                 'name': 'Input'}]

    def theano_outputs(self):
        to_be_output = self.pull_by_index(0)

        print(self.edges_in[0].type)

        if self.edges_in[0].type == 'scalar' or self.edges_in[0].type == 'tensor':
            return [to_be_output]
        elif self.edges_in[0].type == 'list':
            return to_be_output


