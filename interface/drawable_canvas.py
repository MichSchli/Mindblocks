import tkinter as tk

from components.abstract_component import Link
from components.abstract_ui_representation import UIRepresentation
from interface.graphics.graphic import LinkBall
from interface.selection import Selection


class DrawableCanvas(tk.Canvas):

    ui_elements = None
    parent = None
    selected_graph = None
    selected_ui_element = None
    
    def __init__(self, parent, view):
        self.x = self.y = 0
        tk.Canvas.__init__(self, parent, cursor="cross", borderwidth=4, relief='sunken')
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.ui_elements = []

        self.parent = parent
        self.selected_graph = Selection(None)

        self.view = view

    def replace_view(self, new_view):
        self.view = new_view
        self.delete("all")
        self.ui_elements = []
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


    def get_available_modules(self):
        self.view.load_modules()
        return self.view.get_available_modules()

    def on_button_press(self, event):
        x = event.x
        y = event.y

        clicked_ui_element = self.ui_element_at(x, y)
        
        if clicked_ui_element is None and self.selected_ui_element.properties['is_toolbox']:
            new_component = self.view.instantiate(self.selected_ui_element.get())
            new_graphic = self.selected_ui_element.get().instantiate_graphic()
            new_ui_element = UIRepresentation(new_component, new_graphic)

            new_ui_element.set_position(x,y)
            self.ui_elements.append(new_ui_element)
            new_ui_element.draw(self)

            sockets = new_component.in_sockets + new_component.out_sockets
            for socket in sockets:
                socket_graphic = LinkBall()
                socket_ui_element = UIRepresentation(socket, socket_graphic)
                socket_ui_element.draw(self)
                self.ui_elements.append(socket_ui_element)

            self.selected_ui_element.change(new_ui_element, properties={'is_toolbox':False})
            self.selected_graph.change(new_component.get_graph())
        elif clicked_ui_element is None:
            self.selected_ui_element.change(None, properties={'is_toolbox':False})
            self.selected_graph.change(None)
        else:
            if self.should_make_link(self.selected_ui_element.get(), clicked_ui_element):
                self.view.create_edge(self.selected_ui_element.get().component, clicked_ui_element.component)

                c1 = self.selected_ui_element.get()
                c2 = clicked_ui_element

                link_ui_element = c1.link_to(c2)
                self.ui_elements.append(link_ui_element)
                link_ui_element.draw(self)

                self.selected_graph.change(clicked_ui_element.component.get_graph())
            elif self.should_make_link(clicked_ui_element, self.selected_ui_element.get()):
                self.view.create_edge(clicked_ui_element.component, self.selected_ui_element.get().component)

                c1 = clicked_ui_element
                c2 = self.selected_ui_element.get()

                link_ui_element = c1.link_to(c2)
                self.ui_elements.append(link_ui_element)
                link_ui_element.draw(self)

                self.selected_graph.change(clicked_ui_element.get_graph())
            else:
                self.selected_ui_element.change(clicked_ui_element, properties={'is_toolbox':False})
                self.selected_graph.change(clicked_ui_element.component.get_graph())

    def should_make_link(self, c1, c2):
        if c1 is None or c2 is None:
            return False

        c1 = c1.component
        c2 = c2.component
        if c1.__class__.__name__ == 'OutSocket' and c2.__class__.__name__ == 'InSocket':
            print("heh")
            return c1.parent != c2.parent
        return False

    def get_selected_graph(self):
        return self.selected_graph.get()

    def ui_element_at(self, x, y):
        for ui_element in self.ui_elements:
            if ui_element.get_graphic().contains_position((x,y)):
                return ui_element

        return None
        
