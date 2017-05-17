import tkinter as tk

from NEW.observer.selection import Selection
from components.abstract_ui_representation import UIRepresentation
from interface.graphics.graphic import LinkBall


class DrawableCanvas(tk.Canvas):

    ui_elements = None
    parent = None
    selected_graph = None
    selected_ui_element = None
    
    def __init__(self, parent, view, controller):
        self.x = self.y = 0
        tk.Canvas.__init__(self, parent, cursor="cross", borderwidth=4, relief='sunken')
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.ui_elements = []

        self.parent = parent
        self.selected_graph = Selection(None)

        self.view = view
        self.replace_view(view)
        self.controller = controller

    def replace_view(self, new_view):
        self.view = new_view
        self.delete("all")
        self.ui_elements = []

        if self.selected_ui_element is not None:
            self.selected_ui_element.change(None, properties={'is_toolbox':False})
            self.selected_graph.change(None)

        dic_rep = {}

        for graph in self.view.get_defined_graphs():
            for vertex in graph.topological_walk():
                if not vertex.is_socket():
                    module_component = vertex.get_module_component()
                    graphic = module_component.instantiate_graphic()

                    new_ui_element = UIRepresentation(vertex, graphic)
                    self.ui_elements.append(new_ui_element)
                    new_ui_element.draw(self)
                else:
                    socket_graphic = LinkBall()
                    socket_ui_element = UIRepresentation(vertex, socket_graphic)
                    socket_ui_element.draw(self)
                    self.ui_elements.append(socket_ui_element)
                    dic_rep[vertex.get_unique_identifier()] = socket_ui_element

                    if vertex.get_edges_in() and vertex.get_edges_in()[0].origin.is_socket():
                        origin = dic_rep[vertex.get_edges_in()[0].origin.get_unique_identifier()]
                        link_ui_element = origin.link_to(socket_ui_element)
                        self.ui_elements.append(link_ui_element)
                        link_ui_element.draw(self)

    def add_ui_edge(self, edge):
        origin = edge.origin
        destination = edge.destination

        ui_origin = self.get_ui_element(origin)
        ui_destination = self.get_ui_element(destination)

        link_ui_element = ui_origin.link_to(ui_destination)
        link_ui_element.component = edge
        self.ui_elements.append(link_ui_element)
        link_ui_element.draw(self)

    def get_ui_element(self, model):
        uid = model.get_unique_identifier()
        for element in self.ui_elements:
            if element.component.get_unique_identifier() == uid:
                return element
        return None


    def get_available_modules(self):
        self.view.load_modules()
        return self.view.get_available_modules()

    def add_ui_component(self, component, location):
        new_graphic = self.selected_ui_element.get().instantiate_graphic()
        new_ui_element = UIRepresentation(component, new_graphic)

        new_ui_element.set_position(location[0], location[1])
        self.ui_elements.append(new_ui_element)
        new_ui_element.draw(self)

        sockets = component.in_sockets + component.out_sockets
        for socket in sockets:
            socket_graphic = LinkBall()
            socket_ui_element = UIRepresentation(socket, socket_graphic)
            socket_ui_element.draw(self)
            self.ui_elements.append(socket_ui_element)

        self.selected_ui_element.change(new_ui_element, properties={'is_toolbox': False})
        self.selected_graph.change(component.get_graph())

    def on_button_press(self, event):
        x = event.x
        y = event.y

        clicked_ui_element = self.ui_element_at(x, y)
        
        if clicked_ui_element is None and self.selected_ui_element.properties['is_toolbox']:
            module = self.selected_ui_element.get()
            canvas = self.view
            location = (x,y)

            self.controller.create_component_with_sockets(module, canvas, location)

        elif clicked_ui_element is None:
            self.selected_ui_element.change(None, properties={'is_toolbox':False})
            self.selected_graph.change(None)
        else:
            print(clicked_ui_element.component.get_graph())
            if self.should_make_link(self.selected_ui_element.get(), clicked_ui_element):
                c1 = self.selected_ui_element.get().component
                c2 = clicked_ui_element.component
                self.controller.create_edge(c1, c2)
            else:
                self.selected_ui_element.change(clicked_ui_element, properties={'is_toolbox':False})
                self.selected_graph.change(clicked_ui_element.component.get_graph())

    def should_make_link(self, c1, c2):
        if c1 is None or c2 is None:
            return False

        c1 = c1.component
        c2 = c2.component
        if (c1.__class__.__name__ == 'OutSocketModel' and c2.__class__.__name__ == 'InSocketModel') or\
                (c2.__class__.__name__ == 'OutSocketModel' and c1.__class__.__name__ == 'InSocketModel'):
            return True
        return False

    def get_selected_graph(self):
        return self.selected_graph.get()

    def ui_element_at(self, x, y):
        for ui_element in self.ui_elements:
            if ui_element.get_graphic().contains_position((x,y)):
                return ui_element

        return None
        
