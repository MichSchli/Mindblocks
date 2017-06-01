import tkinter as tk
from tkinter import ttk

from NEW.controller.mindblocks_controller import MindblocksController
from NEW.model.graph.graph_runners.python_graph_runner import GraphRunner
from NEW.observer.selection import Selection
from interface.drawable_canvas import DrawableCanvas
from interface.other.description_panel import DescriptionPanel
from interface.other.file_interface import FileInterface
from interface.other.menubar import Menubar
from interface.other.toolbox import Toolbox


#from views.view_manager import ViewManager


class Interface(tk.Tk):

    canvases = []

    def __init__(self):
        tk.Tk.__init__(self)

        '''
        Initialize controller
        '''
        self.controller = MindblocksController(self)

        '''
        Initialize selectors:
        '''
        self.initialize_selectors()

        '''
        Initialize general UI:
        '''
        self.title('Mindblocks')
        self.geometry('{}x{}'.format(800, 600))
        self.menubar = Menubar(self)
        self.config(menu=self.menubar)
        self.make_support_frames()

        '''
        Initialize model-specific UI:
        '''
        self.initialize_toolbox()

        self.controller.update_toolbox()
        self.initialize_description_panel()
        self.initialize_canvas_area()

        '''
        Initialize persistence:
        '''
        #self.graph_saver = GraphSaver()
        #self.view_saver = ViewSaver(self.graph_saver)
        #self.graph_loader = GraphLoader(self.module_importer)
        #self.view_loader = ViewLoader(self.graph_loader, self.module_manager, self.identifier_factory)
        self.file_interface = FileInterface()


        # Create first view:
        self.controller.create_new_canvas()


    def make_support_frames(self):
        self.left_frame = tk.Frame(self, background="blue")
        self.right_frame = tk.Frame(self, background="green")

        self.right_frame.pack(side=tk.RIGHT, expand=False, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.left_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, pady=0, padx=0, anchor="ne")

    '''
    Initialize model-specific UI:
    '''

    def initialize_description_panel(self):
        self.description_panel = DescriptionPanel(self.right_frame)
        self.description_panel.selected_component = self.selected_component
        self.selected_component.set_observer(self.description_panel.component_selection_changed)
        self.description_panel.pack(side=tk.BOTTOM, expand=False, fill=tk.X, pady=0, padx=0, anchor="s")

    def display_modules(self, modules):
        self.toolbox.display_modules(modules)

    def initialize_toolbox(self):
        self.toolbox = Toolbox(self.right_frame)
        self.toolbox.selected_component = self.selected_component
        #self.toolbox.display_modules(self.module_manager.fetch_basic_modules())
        self.toolbox.pack(side=tk.TOP, expand=True, fill=tk.Y, pady=0, padx=0, anchor="n")

    def initialize_canvas_area(self):
        self.note = ttk.Notebook(self.left_frame)
        self.note.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor="nw")

        def tabChangedEvent(event):
            new_canvas_idx = event.widget.index("current")
            new_canvas = self.canvases[new_canvas_idx]
            self.selected_canvas.change(new_canvas)

        self.note.bind_all("<<NotebookTabChanged>>", tabChangedEvent)

    def initialize_selectors(self):
        self.selected_canvas = Selection(None)
        self.selected_component = Selection(None, properties = {'is_toolbox':False})


    '''
    Interface
    '''

    def select_save_file(self):
        outfile = self.file_interface.save_as_file()
        return outfile


    def predict_selection(self):
        graph = self.selected_canvas.get().get_selected_graph()
        result = self.controller.execute_graph(graph)
        print(result)

    def compile_selection(self):
        pass

    def save_current_view(self):
        canvas = self.selected_canvas.get()
        self.controller.save_single_canvas(canvas.view)

    def save_all_views(self):
        outfile = self.file_interface.save_as_file()
        for line in self.view_saver.process(self.agent_canvas.view):
            print(line, file=outfile)

    def load(self):
        infile = self.file_interface.load_file()
        str_rep = infile.read()

        new_view = self.view_loader.load_next_view(str_rep)

        if new_view.name == "agent":
            self.agent_canvas.replace_view(new_view)

    def load_view(self):
        infile = self.file_interface.load_file()
        str_rep = infile.read()

        new_view, _ = self.view_loader.load_next_view(str_rep)
        self.process_view_in_ui(new_view)


    def add_view(self, view_name=None):
        self.controller.create_new_canvas()


    def process_view_in_ui(self, view):
        canvas = DrawableCanvas(self.note, view, self.controller)
        self.note.add(canvas, text=view.get_unique_identifier())
        self.canvases.append(canvas)
        self.selected_canvas.change(canvas)
        canvas.selected_ui_element = self.selected_component
        self.note.select(len(self.canvases) - 1)

    def process_component_in_ui(self, component, location):
        self.selected_canvas.get().add_ui_component(component, location)

    def process_edge_in_ui(self, edge):
        self.selected_canvas.get().add_ui_edge(edge)
