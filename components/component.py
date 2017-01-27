from graph.graph import Graph
from graph.vertex import Vertex
from interface.graphics.graphic import *
import theano.tensor as T

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
        print(self.graphic)
        self.graphic.draw(canvas, self.position)
        for sub_component in self.sub_components:
            sub_component.draw(canvas)

    def set_position(self, x, y):
        self.position = [x,y]
        for sub_component in self.sub_components:
            sub_component.set_position_from_parent()

class Component(Vertex, UIComponent):

    links_in = []
    links_out = []
    source_string = None

    def __init__(self, name=None, identifier=None, create_graph=True):
        if name is not None:
            self.name = name

        self.identifier = identifier

        UIComponent.__init__(self)

        if create_graph:
            Vertex.__init__(self)
            self.create_links()

        
    def get_name(self):
        name_string = self.name
        if self.identifier is not None:
            name_string += "#"+str(self.identifier)
        return name_string

    def create_links(self):
        for description in self.links_in:
            link = InLink(description, self)
            link.add_edge(self)
            self.sub_components.append(link)

        for description in self.links_out:
            link = OutLink(description, self)
            self.add_edge(link)
            self.sub_components.append(link)

    
class Link(Vertex, UIComponent):

    link_radius = 6

    def __init__(self, description, parent):
        self.description = description
        self.parent = parent

        Vertex.__init__(self)
        UIComponent.__init__(self)

    def get_graphic(self):
        return None

    def get_name(self):
        parent_name = self.parent.get_name()
        name = self.description['name']
        return parent_name + '-' + name

    def calculate_position_from_parent(self):
        #TODO this is shit
        vector = np.array(self.description['position'])
        scaled_vector = self.link_radius * vector / np.linalg.norm(vector)
        position = self.parent.position + vector + scaled_vector
        return position[0], position[1]


    def set_position_from_parent(self):
        x, y = self.calculate_position_from_parent()
        self.set_position(x, y)
        
class OutLink(Link):

    partners = []
    
    def get_graphic(self):
        return LinkBall(self.parent.graphic, self.description['position'])

    def link_to(self, in_link):
        self.partners.append(in_link)
        in_link.set_partner(self)
        self.add_edge(in_link)

        #Temporarily we cannot delete components
        return Edge(self, in_link)

    def compile_theano(self):
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
    
class Edge(UIComponent):
    
    def __init__(self, out_link, in_link):
        self.out_link = out_link
        self.in_link = in_link

        UIComponent.__init__(self)
        
    def get_name(self):
        return self.in_link.get_name() + " -> " + self.out_link.get_name()

    def get_graphic(self):
        return EdgeLine(self.out_link.graphic, self.in_link.graphic)
