import tkinter as tk

class DrawableCanvas(tk.Canvas):

    def __init__(self, parent):
        self.x = self.y = 0
        tk.Canvas.__init__(self, parent, width=200, height=200, cursor="cross")
        self.pack(side="top", fill="both", expand=True)
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_button_release(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)

        self.create_rectangle(x0,y0,x1,y1, fill=self.color)

