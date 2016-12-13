import tkinter as tk

class DrawableCanvas(tk.Canvas):

    components = None
    graphs = []
    
    def __init__(self, parent):
        self.x = self.y = 0
        tk.Canvas.__init__(self, parent, cursor="cross", borderwidth=4, relief='sunken')
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.components = []

    def on_button_press(self, event):
        x = event.x
        y = event.y

        clicked_component = self.component_at(x,y)
        
        if clicked_component is None and self.selected_component.properties['is_toolbox']:
            new_component = self.selected_component.get().copy(identifier=len(self.components))
            self.components.append(new_component)
            self.components.extend(new_component.get_sub_components())

            self.graphs.append(new_component.get_graph())

            new_component.set_position(x,y)
            new_component.draw(self)
                                  
            self.selected_component.change(new_component, properties={'is_toolbox':False})
        else:
            if self.should_make_link(self.selected_component.get(), clicked_component):
                self.make_link(self.selected_component.get(), clicked_component)
            elif self.should_make_link(clicked_component, self.selected_component.get()):
                self.make_link(clicked_component, self.selected_component.get())
            else:    
                self.selected_component.change(clicked_component, properties={'is_toolbox':False})    

    def should_make_link(self, c1, c2):
        return c1.__class__.__name__ == 'OutLink' and c2.__class__.__name__ == 'InLink'

    def make_link(self, c1, c2):
        link = c1.link_to(c2)
        self.components.append(link)
        link.graphic.draw(self, None)
    
    def component_at(self, x, y):
        for component in self.components:
            if component.graphic.contains_position((x,y)):
                return component

        return None
        
