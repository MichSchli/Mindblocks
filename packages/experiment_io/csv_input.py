import numpy as np

from assorted.GraphInput import GraphInput
from model.component.component_model import ComponentModel


class CsvInput(ComponentModel):
    name = "CsvInput"
    default_out_sockets = [{'position': [0, -20],
                  'name': 'Output'}]

    default_attributes = {'path': '<argument>',
                  'n_columns': '3',
                  'separator': ','}

    graph_input = None

    def __init__(self, manifest=None, identifier=None):
        ComponentModel.__init__(self, manifest=manifest, identifier=identifier)
        self.graph_input = GraphInput(self.get_name()+"_input", [3])

    def parse_column_string(self, string):
        return np.fromstring(string, sep=' ', dtype=np.int32)

    def theano_inputs(self):
        return [self.graph_input]

    def compile_theano(self):
        self.graph_input.compile_theano()
        self.push_by_index(0, self.graph_input.variable)

