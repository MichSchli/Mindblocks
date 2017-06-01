import numpy as np

from NEW.model.graph.vertex_model import VertexModel
from NEW.model.identifiables.identifiable import Identifiable


class AbstractSocketModel(Identifiable, VertexModel):

    parent_component = None
    link_radius = 6
    description = None
    attributes = None

    def __init__(self, unique_identifier):
        VertexModel.__init__(self)
        Identifiable.__init__(self, unique_identifier=unique_identifier)
        self.attributes = {}

    def is_socket(self):
        return True

    def calculate_position_from_parent(self, parent_position):
        vector = np.array(self.description['position'])
        scaled_vector = self.link_radius * vector / np.linalg.norm(vector)
        position = parent_position + vector + scaled_vector
        return position[0], position[1]

    def get_position(self):
        parent_position = self.parent_component.get_position()
        return self.calculate_position_from_parent(parent_position)

    def get_attributes(self):
        return self.attributes

    def get_parent_component(self):
        return self.parent_component

    def parse_attributes(self):
        return True