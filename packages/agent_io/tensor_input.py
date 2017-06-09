import numpy as np

from assorted.GraphInput import GraphInput
from model.component.component_model import ComponentModel


class TensorInput(ComponentModel):

    name = "TensorInput"
    default_out_sockets = [{'position': [0, -20],
                 'name': 'Output'}]

    default_attributes = {'dimension': '1'}
    parsed_attributes = None
    variable = None

    def compile_theano(self):
        graph_input = GraphInput(self.get_name(), self.parsed_attributes['dimension'])
        self.variable = graph_input.compile_theano()
        self.push_by_index(0, self.variable)

    def parse_dimension_string(self, string):
        return np.fromstring(string, sep=' ', dtype=np.int32)

    def parse_attributes(self):
        d = {'dimension': self.parse_dimension_string(self.attributes['dimension'])}

        for k in d:
            if d[k] is None:
                return False

        self.parsed_attributes = d

        return True

    def get_theano_inputs(self):
        return [(self.get_unique_identifier() + "_variable", self.variable)]
