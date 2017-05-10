from components.abstract_socket import InSocket, OutSocket
from graph.graph import Graph
from graph.vertex import Vertex
from interface.graphics.graphic import *
import theano.tensor as T
from identifiables.identifiable import Identifiable
from components.abstract_ui_representation import *

class Component(Vertex, Identifiable):

    default_in_sockets = []
    default_out_sockets = []
    source_string = None
    default_attributes = {}
    chosen_language = None
    position = None

    in_sockets = []
    out_sockets = []

    def __init__(self, manifest=None, identifier=None, module=None):
        Vertex.__init__(self, name=self.name)

        self.name = manifest['name']
        self.manifest = manifest
        self.chosen_language = self.manifest['languages'][0]
        self.attributes = self.default_attributes
        self.module = module


    def update_attributes(self, new_attributes):
        for k,v in new_attributes.items():
            self.attributes[k] = v

        if 'x' in self.attributes and 'y' in new_attributes:
            x = int(self.attributes['x'])
            y = int(self.attributes['y'])

            self.set_position(x,y)

    def set_position(self, x, y):
        self.attributes['x'] = str(x)
        self.attributes['y'] = str(y)
        self.position = [x,y]

    def get_module_component(self):
        return self.module

    def get_position(self):
        return self.position

    def create_sockets(self):
        self.in_sockets = []
        for description in self.default_in_sockets:
            link = InSocket(self, description)
            link.add_edge(self)
            self.in_sockets.append(link)

        self.out_sockets = []
        for description in self.default_out_sockets:
            link = OutSocket(self, description)
            self.add_edge(link)
            self.out_sockets.append(link)


    def get_out_socket_by_id(self, id):
        return self.get_edges_out()[id].destination

    def get_in_socket_by_id(self, id):
        return self.get_edges_in()[id].origin

    def get_out_socket_by_name(self, name):
        for edge in self.get_edges_out():
            if edge.destination.description['name'] == name:
                return edge.destination
        return None

    def get_in_socket_by_name(self, name):
        for edge in self.get_edges_in():
            if edge.origin.description['name'] == name:
                return edge.origin
        return None




