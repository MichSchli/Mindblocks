import tkinter as tk

class DrawableCanvas(tk.Canvas):

    def __init__(self, parent):
        self.x = self.y = 0
        tk.Canvas.__init__(self, parent, cursor="cross", borderwidth=4, relief='sunken')
        self.bind("<ButtonPress-1>", self.on_button_press)

    def on_button_press(self, event):
        x = event.x
        y = event.y

        current_component = self.toolbox.selection
        if current_component is not None:
            current_component.copy().draw(self, (x,y))

