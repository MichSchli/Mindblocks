import tkinter as tk

from interface.selection import Selection


class DrawableCanvas(tk.Canvas):

    components = None
    parent = None
    selected_graph = None
    
    def __init__(self, parent, view):
        self.x = self.y = 0
        tk.Canvas.__init__(self, parent, cursor="cross", borderwidth=4, relief='sunken')
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.components = []

        self.parent = parent
        self.selected_graph = Selection(None)

        self.view = view

    def get_available_modules(self):
        self.view.load_modules()
        return self.view.get_available_modules()

    def on_button_press(self, event):
        x = event.x
        y = event.y

        clicked_component = self.component_at(x,y)
        
        if clicked_component is None and self.selected_component.properties['is_toolbox']:
            new_component = self.view.instantiate(self.selected_component.get())

            self.components.append(new_component)
            self.components.extend(new_component.get_sub_components())

            new_component.set_position(x,y)
            new_component.draw(self)
                                  
            self.selected_component.change(new_component, properties={'is_toolbox':False})
            self.selected_graph.change(new_component.get_graph())
        elif clicked_component is None:
            self.selected_component.change(None, properties={'is_toolbox':False})
            self.selected_graph.change(None)
        else:
            if self.should_make_link(self.selected_component.get(), clicked_component):
                self.view.create_edge(self.selected_component.get(), clicked_component)

                c1 = self.selected_component.get()
                c2 = clicked_component

                link = c1.link_to(c2)
                self.components.append(link)
                link.graphic.draw(self, None)

                self.selected_graph.change(clicked_component.get_graph())
            elif self.should_make_link(clicked_component, self.selected_component.get()):
                self.view.create_edge(clicked_component, self.selected_component.get())

                c1 = clicked_component
                c2 = self.selected_component.get()

                link = c1.link_to(c2)
                self.components.append(link)
                link.graphic.draw(self, None)

                self.selected_graph.change(clicked_component.get_graph())
            else:
                self.selected_component.change(clicked_component, properties={'is_toolbox':False})
                self.selected_graph.change(clicked_component.get_graph())

    def should_make_link(self, c1, c2):
        return c1.__class__.__name__ == 'OutLink' and c2.__class__.__name__ == 'InLink'

    def get_selected_graph(self):
        return self.selected_graph.get()

    def make_link(self, c1, c2):
        self.module_manager.delete_graph(self.view_name, c2.get_graph())
        link = c1.link_to(c2)
        self.components.append(link)
        link.graphic.draw(self, None)
    
    def component_at(self, x, y):
        for component in self.components:
            if component.graphic.contains_position((x,y)):
                return component

        return None
        
