import tkinter as tk
import math

from observables.observable import Observable
from observables.observed_event import ObservedEvent


class Toolbox(tk.Frame, Observable):

    components = []
    canvas = None
    modules = []

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=200)
        self.set_canvas()
        Observable.__init__(self, events=['clicked'])
        
    def set_canvas(self):
        self.canvas = ToolboxCanvas(self)

        self.canvas.scrollbar.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        
    def display_modules(self, modules):
        self.modules = modules
        self.update_components()

    def set_selection(self, component):
        toolbox_property = component is not None
        
    def clicked(self, component):
        event = ObservedEvent('clicked')
        event.component = component
        self.notify_observers(event)

    def update_components(self):
        self.canvas.set_modules(self.modules)

    def define_click_observer(self, observer):
        self.define_observer(observer, event='clicked')


class ToolboxCanvas(tk.Canvas):

    border_width = 5
    module_areas = []
    
    def __init__(self, parent):
        self.scrollbar = tk.Scrollbar(parent)
        tk.Canvas.__init__(self, parent, width=201, cursor="cross", borderwidth=self.border_width, relief='sunken', yscrollcommand=self.scrollbar.set)
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.scrollbar.config(command=self.yview)
        self.parent = parent

    def set_modules(self, modules):
        self.module_areas = []
        for module in modules:
            module_area = ComponentArea(self, module)
            self.module_areas.append(module_area)

        self.draw_modules()

    def draw_modules(self):
        self.delete("all")

        offset = 0
        for module_area in self.module_areas:
            module_area.draw(offset=offset)
            offset += module_area.get_height()

        self.config(scrollregion=(0, 0, 200 + self.border_width * 2, offset + self.border_width))

    def on_button_press(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)

        offset = 0
        for module_area in self.module_areas:
            if y < offset + module_area.get_height():
                module_area.click(x-6,y-offset)
                break
            else:
                offset += module_area.get_height()



class ComponentArea:

    active = False

    def __init__(self, canvas, module):
        self.canvas = canvas
        self.module = module

        self.header = SeparatorBar(canvas, module.get_name())

        self.component_slices = [ComponentSlice(self.canvas, component) for component in module.get_components()]

    def draw(self, offset=6):
        self.header.draw(y_offset=offset)
        offset += self.header.get_height()
        if self.active:
            self.draw_components(offset)

    def draw_components(self, offset):
        position = [6,offset]
        odd = False
        for slice in self.component_slices:
            slice.draw(position)
            odd = not odd

            if odd:
                position[0] += 100
            else:
                position[0] -= 100
                position[1] += 100


    def get_height(self):
        height = self.header.get_height()
        if self.active:
            height += math.ceil(len(self.component_slices) / 2)*100
        return height

    def toggle(self):
        self.active = not self.active
        self.canvas.draw_modules()

    def click(self, x, y):
        if y < self.header.get_height():
            self.toggle()
        else:
            y -= self.header.get_height()
            slice = math.floor(x / 100) + math.floor(y / 100) * 2
            self.component_slices[slice].click(x % 100,y % 100)



class SeparatorBar:

    default_width = 200
    default_height = 26

    def __init__(self, canvas, name):
        self.canvas = canvas
        self.name = name

    def get_coords(self, x_offset, y_offset):
        return 0 + x_offset, 0 + y_offset, self.default_width + x_offset, self.default_height + y_offset

    def get_text_coords(self, x_offset, y_offset):
        return self.default_width / 2 + x_offset, self.default_height / 2 + y_offset

    def draw(self, x_offset=6, y_offset=6):
        self.canvas.create_rectangle(*self.get_coords(x_offset, y_offset))
        text_coords = self.get_text_coords(x_offset, y_offset)
        self.canvas.create_text(text_coords[0], text_coords[1], text=self.name)

    def get_height(self):
        return self.default_height

class ComponentSlice():

    padding = 10

    def __init__(self, canvas, component):
        self.component = component
        self.canvas = canvas

    def draw(self, position):
        x = position[0]
        y = position[1]

        x_max_size = 100 - self.padding * 2
        y_max_size = 100 - self.padding * 2

        x_center = x + 50
        y_center = y + 50

        self.component.instantiate_graphic().draw(self.canvas, (x_center, y_center), fit_to_size=(x_max_size, y_max_size))

    def click(self, x, y):
        self.canvas.parent.clicked(self.component)
        
