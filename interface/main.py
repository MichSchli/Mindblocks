import tkinter as tk
import imp

network = imp.load_source('network','interface/network_canvas/network_canvas.py')
optimizer = imp.load_source('optimizer','interface/optimizer_canvas/optimizer_canvas.py')
dataset = imp.load_source('dataset','interface/dataset_canvas/dataset_canvas.py')



class Interface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.add_canvases()

    def add_canvases(self):
        self.network_canvas = network.NetworkCanvas(self)
        self.optimizer_canvas = optimizer.OptimizerCanvas(self)
        self.dataset_canvas = dataset.DatasetCanvas(self)
