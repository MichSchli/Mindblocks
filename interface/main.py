import tkinter as tk
from tkinter import ttk
import imp

selection = imp.load_source('selection', 'interface/selection.py')
network = imp.load_source('network','interface/network_canvas/network_canvas.py')
optimizer = imp.load_source('optimizer','interface/optimizer_canvas/optimizer_canvas.py')
dataset = imp.load_source('dataset','interface/dataset_canvas/dataset_canvas.py')

graphics = imp.load_source('graphics','interface/graphics/graphic.py')

menu = imp.load_source('menu','interface/other/menubar.py')
toolbox = imp.load_source('toolbox','interface/other/toolbox.py')
description = imp.load_source('toolbox','interface/other/description_panel.py')

graph = imp.load_source('graph', 'graph/graph.py')

class Interface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title('Mindblocks')
        self.geometry('{}x{}'.format(800, 600))

        self.selected_component = selection.Selection(None)
        
        self.menubar = menu.Menubar(self)
        self.config(menu=self.menubar)
        
        self.make_support_frames()
        self.add_canvases()
        self.add_interface()

        self.initialize_component_selection()
        self.initialize_canvas_selection()

        return


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
        

    def make_support_frames(self):
        self.left_frame = tk.Frame(self, background="blue")
        self.right_frame = tk.Frame(self, background="green")

        self.right_frame.pack(side=tk.RIGHT, expand=False, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.left_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, pady=0, padx=0, anchor="ne")

    def add_interface(self):
        self.toolbox = toolbox.Toolbox(self.right_frame)
        self.description_panel = description.DescriptionPanel(self.right_frame)

        self.description_panel.pack(side=tk.BOTTOM, expand=False, fill=tk.X, pady=0, padx=0, anchor="s")
        self.toolbox.pack(side=tk.BOTTOM, expand=True, fill=tk.Y, pady=0, padx=0, anchor="n")

    def initialize_canvas_selection(self):
        self.selected_canvas = selection.Selection(self.network_canvas)
        self.selected_canvas.set_watcher(self.toolbox.canvas_selection_changed) 
        
        def tabChangedEvent(event):
            if event.widget.index("current") == 0:
                self.selected_canvas.change(self.network_canvas)
            elif event.widget.index("current") == 1:
                self.selected_canvas.change(self.optimizer_canvas)
            elif event.widget.index("current") == 2:
                self.selected_canvas.change(self.dataset_canvas)
                        
        self.note.bind_all("<<NotebookTabChanged>>", tabChangedEvent)

    def initialize_component_selection(self):
        self.selected_component = selection.Selection(None, properties = {'is_toolbox':False})
        self.network_canvas.selected_component = self.selected_component
        self.optimizer_canvas.selected_component = self.selected_component
        self.dataset_canvas.selected_component = self.selected_component
        self.toolbox.selected_component = self.selected_component
        self.description_panel.selected_component = self.selected_component

        self.selected_component.set_watcher(self.description_panel.component_selection_changed) 
        

    def predict_selection(self):
        self.selection.predict()
        
    def add_canvases(self):
        self.note = ttk.Notebook(self.left_frame)
        
        self.network_canvas = network.NetworkCanvas(self.note)
        self.optimizer_canvas = optimizer.OptimizerCanvas(self.note)
        self.dataset_canvas = dataset.DatasetCanvas(self.note)

        self.note.add(self.network_canvas, text="Network")
        self.note.add(self.optimizer_canvas, text="Optimizer")
        self.note.add(self.dataset_canvas, text="Datasets")
        
        self.note.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor="nw")


    def layout(self):
        self.description_panel.pack(side=tk.BOTTOM, expand=False, pady=0, padx=0, anchor="se")
        self.toolbox.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.note.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, pady=0, padx=0, anchor="ne")
