import tkinter as tk
from tkinter import ttk
import imp

network = imp.load_source('network','interface/network_canvas/network_canvas.py')
optimizer = imp.load_source('optimizer','interface/optimizer_canvas/optimizer_canvas.py')
dataset = imp.load_source('dataset','interface/dataset_canvas/dataset_canvas.py')

menu = imp.load_source('menu','interface/other/menubar.py')



class Interface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.add_canvases()

        self.menubar = menu.Menubar(self)
        self.config(menu=self.menubar)

    def add_canvases(self):
        self.note = ttk.Notebook(self)
        
        self.network_canvas = network.NetworkCanvas(self.note)
        self.optimizer_canvas = optimizer.OptimizerCanvas(self.note)
        self.dataset_canvas = dataset.DatasetCanvas(self.note)

        self.note.add(self.network_canvas, text="Network")
        self.note.add(self.optimizer_canvas, text="Optimizer")
        self.note.add(self.dataset_canvas, text="Datasets")

        self.note.pack()
