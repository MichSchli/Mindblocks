import tkinter as tk
from tkinter import ttk
import imp

selection = imp.load_source('selection', 'interface/selection.py')
network = imp.load_source('network','interface/network_canvas/network_canvas.py')
dataset = imp.load_source('dataset','interface/preprocessing_canvas/preprocessing_canvas.py')

graphics = imp.load_source('graphics','interface/graphics/graphic.py')

menu = imp.load_source('menu','interface/other/menubar.py')
toolbox = imp.load_source('toolbox','interface/other/toolbox.py')
description = imp.load_source('toolbox','interface/other/description_panel.py')


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
                self.selected_canvas.change(self.preprocessing_canvas)
                        
        self.note.bind_all("<<NotebookTabChanged>>", tabChangedEvent)

    def initialize_component_selection(self):
        self.selected_component = selection.Selection(None, properties = {'is_toolbox':False})
        self.network_canvas.selected_component = self.selected_component
        self.preprocessing_canvas.selected_component = self.selected_component
        self.toolbox.selected_component = self.selected_component
        self.description_panel.selected_component = self.selected_component

        self.selected_component.set_watcher(self.description_panel.component_selection_changed) 
        

    def predict_selection(self):
        graph = self.network_canvas.get_selected_graph()
        predict_function = graph.compile_theano(mode='predict')
        print(predict_function())

        
    def add_canvases(self):
        self.note = ttk.Notebook(self.left_frame)
        
        self.network_canvas = network.NetworkCanvas(self.note)
        self.preprocessing_canvas = dataset.DatasetCanvas(self.note)

        self.note.add(self.network_canvas, text="Network")
        self.note.add(self.preprocessing_canvas, text="Preprocessing")
        
        self.note.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor="nw")


    def layout(self):
        self.description_panel.pack(side=tk.BOTTOM, expand=False, pady=0, padx=0, anchor="se")
        self.toolbox.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.note.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, pady=0, padx=0, anchor="ne")
