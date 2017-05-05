from graph.graph import Graph
from graph.vertex import Vertex
from interface.graphics.graphic import *
import theano.tensor as T
from identifiables.identifiable import Identifiable

class UIComponent:

    position = None

    def __init__(self):
        self.graphic = self.get_graphic()
        self.sub_components = []

    def get_graphic(self):
        return PlaceholderGraphic(self.name)

    def get_sub_components(self):
        return self.sub_components

    def draw(self, canvas):
        self.graphic.draw(canvas, self.position)
        for sub_component in self.sub_components:
            sub_component.draw(canvas)

    def set_position(self, x, y):
        self.position = [x,y]
        for sub_component in self.sub_components:
            sub_component.set_position_from_parent()

class Component(Vertex, UIComponent, Identifiable):

    links_in = []
    links_out = []
    source_string = None
    default_attributes = {}
    chosen_language = None

    def __init__(self, manifest=None, identifier=None, create_graph=True):
        self.name = manifest['name']
        self.manifest = manifest

        self.chosen_language = self.manifest['languages'][0]

        UIComponent.__init__(self)

        if create_graph:
            Vertex.__init__(self, name=self.name)
            self.create_links()
        else:
            Identifiable.__init__(self, name=self.name)

        self.attributes = self.default_attributes

    def set_position(self, x, y):
        self.attributes['x'] = str(x)
        self.attributes['y'] = str(y)
        UIComponent.set_position(self, x, y)

    def create_links(self):
        for description in self.links_in:
            link = InLink(description, self)
            link.add_edge(self)
            self.sub_components.append(link)

        for description in self.links_out:
            link = OutLink(description, self)
            self.add_edge(link)
            self.sub_components.append(link)

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

class Link(Vertex, UIComponent):

    link_radius = 6

    def __init__(self, description=None, parent=None):
        self.description = description
        self.parent = parent

        Vertex.__init__(self, name=self.name)

        if description is not None:
            UIComponent.__init__(self)

    def get_unique_identifier(self):
        return self.parent.get_unique_identifier() + ':' + self.description['name']

    def get_graphic(self):
        return None

    def is_socket(self):
        return True

    def calculate_position_from_parent(self):
        #TODO this is shit
        vector = np.array(self.description['position'])
        scaled_vector = self.link_radius * vector / np.linalg.norm(vector)
        position = self.parent.position + vector + scaled_vector
        return position[0], position[1]


    def set_position_from_parent(self):
        x, y = self.calculate_position_from_parent()
        self.set_position(x, y)


    def get_python_import(self):
        yield None

    def python_init(self, arguments={}):
        yield None


class OutLink(Link):

    partners = []
    
    def get_graphic(self):
        return LinkBall(self.parent.graphic, self.description['position'])

    def link_to(self, in_link):
        self.partners.append(in_link)
        in_link.set_partner(self)

        #Temporarily we cannot delete components
        return Edge(self, in_link)

    def compile_theano(self):
        value = self.pull_by_index(0)

        for edge in self.get_edges_out():
            edge.push(value, self.get_edges_in()[0].type)


    def compile_python(self):
        value = self.pull_by_index(0)

        for edge in self.get_edges_out():
            edge.push(value, self.get_edges_in()[0].type)


class InLink(Link):

    partner = None
    edge = None

    def get_graphic(self):
        return LinkBall(self.parent.graphic, self.description['position'])

    def set_partner(self, out_link):
        self.partner = out_link

    def compile_theano(self):
        if len(self.get_edges_in()) == 1:
            self.push_by_index(0, self.pull_by_index(0), self.get_edges_in()[0].type)
        else:
            values = [edge.pull() for edge in self.get_edges_in()]
            concatenated = T.concatenate(values, axis=-1)
            self.push_by_index(0, concatenated)

    def compile_python(self):
        if len(self.get_edges_in()) == 1:
            self.push_by_index(0, self.pull_by_index(0), self.get_edges_in()[0].type)
        else:
            values = [edge.pull() for edge in self.get_edges_in()]
            self.push_by_index(0, values)


    
class Edge(UIComponent):
    
    def __init__(self, out_link, in_link):
        self.out_link = out_link
        self.in_link = in_link

        UIComponent.__init__(self)
        
    def get_name(self):
        return self.in_link.get_name() + " -> " + self.out_link.get_name()

    def get_graphic(self):
        return EdgeLine(self.out_link.graphic, self.in_link.graphic)
