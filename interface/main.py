import tkinter as tk
from tkinter import ttk
import imp

network = imp.load_source('network','interface/network_canvas/network_canvas.py')
optimizer = imp.load_source('optimizer','interface/optimizer_canvas/optimizer_canvas.py')
dataset = imp.load_source('dataset','interface/dataset_canvas/dataset_canvas.py')

menu = imp.load_source('menu','interface/other/menubar.py')
toolbox = imp.load_source('toolbox','interface/other/toolbox.py')

graph = imp.load_source('graph', 'graph/graph.py')

class Interface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title('Mindblocks')
        self.geometry('{}x{}'.format(600, 400))

        self.add_canvases()

        self.menubar = menu.Menubar(self)
        self.config(menu=self.menubar)

        self.layout()

        '''
        Temporary graph: output a constant, no training
        '''
        
        self.selection = graph.Graph()

        const = graph.Constant(5)
        out = graph.Output()

        self.selection.add_node(const)
        self.selection.add_node(out)

        const.get_links_out()[0].put(out.get_links_in()[0])
        


    def predict_selection(self):
        self.selection.predict()
        
    def add_canvases(self):
        self.note = ttk.Notebook(self)
        
        self.network_canvas = network.NetworkCanvas(self.note)
        self.optimizer_canvas = optimizer.OptimizerCanvas(self.note)
        self.dataset_canvas = dataset.DatasetCanvas(self.note)

        self.note.add(self.network_canvas, text="Network")
        self.note.add(self.optimizer_canvas, text="Optimizer")
        self.note.add(self.dataset_canvas, text="Datasets")

        #self.note.pack()

        self.toolbox = toolbox.Toolbox(self)

    def layout(self):
        self.toolbox.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.note.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, pady=0, padx=0, anchor="ne")
