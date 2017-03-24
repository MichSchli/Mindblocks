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
    attributes = {}
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

    def create_links(self):
        for description in self.links_in:
            link = InLink(description, self)
            link.add_edge(self)
            self.sub_components.append(link)

        for description in self.links_out:
            link = OutLink(description, self)
            self.add_edge(link)
            self.sub_components.append(link)

    def get_attributes(self):
        return self.attributes

    def python_init(self, arguments={}):
        yield "manifest = "+str(self.manifest)
        yield self.get_unique_identifier() + " = " +  self.__class__.__name__ + "(manifest=manifest)"
        yield arguments['name'] + ".merge(" + self.get_unique_identifier() + ".get_graph())"
        if self.attributes != {}:
            yield self.get_unique_identifier() + ".attributes = " + str(self.attributes)
        for enumerator, in_edge in enumerate(self.edges_in):
            yield in_edge.origin.get_unique_identifier() + " = " + self.get_unique_identifier() + ".edges_in[" + str(enumerator) + "].origin"
        for enumerator, out_edge in enumerate(self.edges_out):
            yield out_edge.destination.get_unique_identifier() + " = " + self.get_unique_identifier() + ".edges_out[" + str(enumerator) + "].destination"

        for in_edge in self.edges_in:
            in_link = in_edge.origin
            for x in in_link.edges_in:
                yield arguments['name'] + ".add_edge(" + x.origin.get_name() + ", " + in_link.get_name() + ")"
        yield ""

    def get_python_import(self):
        yield "from " + self.module + " import " + self.__class__.__name__



class Link(Vertex, UIComponent):

    link_radius = 6

    def __init__(self, description=None, parent=None):
        self.description = description
        self.parent = parent

        self.name = parent.get_name() + '_' + description['name']

        Vertex.__init__(self, name=self.name)

        if description is not None:
            UIComponent.__init__(self)

    def get_graphic(self):
        return None

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
