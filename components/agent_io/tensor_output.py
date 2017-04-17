from components.component import Component

class TensorOutput(Component):

    name = "TensorOutput"
    links_in = [{'position': [0,20],
                 'name': 'Input'}]

    attributes = {}

    def theano_outputs(self):
        to_be_output = self.pull_by_index(0)

        yield (self.get_unique_identifier() + "_output", to_be_output)

