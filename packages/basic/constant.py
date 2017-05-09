import numpy as np
import theano
from components.abstract_component import Component


class Constant(Component):
    name = "Constant"
    default_out_sockets = [{'position': [0, -20],
                  'name': 'Output'}]

    default_attributes = {'value': '0'}
    parsed_attributes = None

    def compile_theano(self):
        self.push_by_index(0, theano.tensor.constant(self.parsed_attributes['value']))

    def compile_python(self):
        self.push_by_index(0, self.parsed_attributes['value'])

    def parse_value_string(self, string):
        return np.fromstring(string, sep=' ', dtype=np.float32)

    def parse_attributes(self):
        d = {'value': self.parse_value_string(self.attributes['value'])}

        for k in d:
            if d[k] is None:
                return False

        self.parsed_attributes = d

        return True
