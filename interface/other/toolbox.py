import tkinter as tk

class Toolbox(tk.Frame):

    components = []
    canvas = None
    selection = None

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=200)
        self.set_canvas()
        
    def set_canvas(self):
        self.canvas = ToolboxCanvas(self)

        self.canvas.scrollbar.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        
    def display_list(self, component_list):
        self.components = component_list
        self.update_components()

    def set_selection(self, component):
        self.selection = component
        
    def clicked(self, component):
        self.set_selection(component)
        print(str(component)+" was clicked!")

    def update_components(self):
        self.set_selection(None)
        self.canvas.set_components(self.components)


class ToolboxCanvas(tk.Canvas):

    border_width = 5
    
    def __init__(self, parent):
        self.scrollbar = tk.Scrollbar(parent)
        tk.Canvas.__init__(self, parent, width=200, cursor="cross", borderwidth=self.border_width, relief='sunken', yscrollcommand=self.scrollbar.set)
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.scrollbar.config(command=self.yview)
        self.next_position = [0,0]
        self.parent = parent

        
    def on_button_press(self, event):
        click = (event.x, event.y)
        clicked_slice = (int((event.x - self.border_width) / 100), int((event.y - self.border_width) / 100))
        clicked_slice_idx = clicked_slice[0] + clicked_slice[1]*2        

        if len(self.component_slices) <= clicked_slice_idx or not self.component_slices[clicked_slice_idx].click(click):
            self.parent.clicked(None)
        else:
            self.parent.clicked(self.component_slices[clicked_slice_idx].component)
        
    def set_components(self, components):
        n_rows = len(components) / 2 + len(components) % 2
        self.reset(n_rows)

        for component in components:
            self.draw_component(component)

    def draw_component(self, component):
        self.component_slices.append(ComponentSlice(component, self, self.next_position))
        self.component_slices[-1].draw()
        self.update_position()

    def update_position(self):
        if self.next_position[1] == 0:
            self.next_position[1] = 1
        else:
            self.next_position[1] = 0
            self.next_position[0] += 1
            
    def reset(self, new_rows):
        self.delete("all")
        self.config(scrollregion=(0, 0, 200+self.border_width*2, new_rows*100+self.border_width*2))
        self.next_position = [0,0]
        self.component_slices = []


class ComponentSlice():

    padding = 10

    def __init__(self, component, canvas, position):
        self.component = component
        self.canvas = canvas
        self.position = position

    def draw(self):
        x = self.position[1]*100+self.canvas.border_width
        y = self.position[0]*100+self.canvas.border_width

        x_max_size = 100 - self.padding * 2
        y_max_size = 100 - self.padding * 2

        x_center = x + 50
        y_center = y + 50

        self.component.draw(self.canvas, (x_center, y_center), fit_to_size=(x_max_size, y_max_size))

    def click(self, position):
        return self.component.contains_position(position)
        
