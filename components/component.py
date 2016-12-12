import imp

graphics = imp.load_source('graphics', 'interface/graphics/graphic.py')
computation = imp.load_source('graph', 'graph/graph.py')

class Component():

    def __init__(self, name=None, identifier=None):
        if name is not None:
            self.name = name

        self.identifier = identifier
        self.graphic = self.get_graphic()
        self.representation = self.get_representation()

        self.create_links()

    def initialize_singleton_graph(self):
        self.graph = computation.Singleton(self)
        return self.graph
    
    def get_links(self):
        return self.in_links + self.out_links

    def get_links_in(self):
        return []

    def get_links_out(self):
        return []        

    def get_representation(self):
        return computation.Node()
        
    def get_name(self):
        name_string = self.name
        if self.identifier is not None:
            name_string += "#"+str(self.identifier)
        return name_string
    
    def get_graphic(self):
        return graphics.PlaceholderGraphic(self.name)

    def create_links(self):
        self.in_links = [InLink(desc, self) for desc in self.get_links_in()]
        self.out_links = [OutLink(desc, self) for desc in self.get_links_out()]
    
    
class Placeholder(Component):
    
    def copy(self, identifier=None):
        return Placeholder(self.name, identifier)
    
class Link(Component):

    def __init__(self, description, parent):
        self.description = description
        self.parent = parent
        self.graphic = self.get_graphic()

    def get_name(self):
        parent_name = self.parent.get_name()
        name = self.description['name']
        return parent_name + '-' + name
        
class OutLink(Link):

    partners = []
    
    def get_graphic(self):
        return graphics.Link(self.parent.graphic, self.description['position'])

    def link_to(self, in_link):
        self.partners.append(in_link)
        in_link.set_partner(self)

        #Temporarily we cannot delete components
        return Edge(self, in_link)

class InLink(Link):

    partner = None
    edge = None

    def get_graphic(self):
        return graphics.Link(self.parent.graphic, self.description['position'])

    def set_partner(self, out_link):
        self.partner = out_link
    
class Edge(Component):
    
    def __init__(self, out_link, in_link):
        self.out_link = out_link
        self.in_link = in_link
        self.graphic = self.get_graphic()
        
    def get_name(self):
        return self.in_link.get_name() + " -> " + self.out_link.get_name()

    def get_graphic(self):
        return graphics.Edge(self.out_link.graphic, self.in_link.graphic)
