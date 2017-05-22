from NEW.model.component.component_model import ComponentModel

class TensorOutput(ComponentModel):

    name = "TensorOutput"
    default_in_sockets = [{'position': [0, 20],
                 'name': 'Input'}]

    default_attributes = {}

    def theano_outputs(self):
        to_be_output = self.pull_by_index(0)

        yield (self.get_unique_identifier() + "_output", to_be_output)

