from model.component.component_model import ComponentModel

class TensorOutput(ComponentModel):

    name = "TensorOutput"
    default_in_sockets = [{'position': [0, 20],
                 'name': 'Input'}]

    default_attributes = {}

    def get_theano_outputs(self):
        to_be_output = self.pull_by_index(0)

        return [(self.get_unique_identifier() + "_output", to_be_output)]

