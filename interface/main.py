import tkinter as tk
from tkinter import ttk

from compilation.compiler import Compiler
from compilation.graph_compiler import GraphCompiler
from graph_runners.python_graph_runner import GraphRunner
from identifiables.identifierFactory import IdentifierFactory
from interface.drawable_canvas import DrawableCanvas
from interface.other.description_panel import DescriptionPanel
from interface.other.file_interface import FileInterface
from interface.other.menubar import Menubar
from interface.other.toolbox import Toolbox
from interface.selection import Selection
from module_management.module_importer import ModuleImporter
from module_management.module_manager import ModuleManager
from persistence.graph_loader import GraphLoader
from persistence.graph_saver import GraphSaver
from persistence.view_loader import ViewLoader
from persistence.view_saver import ViewSaver
from views.view import View


class Interface(tk.Tk):

    canvases = []

    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title('Mindblocks')
        self.geometry('{}x{}'.format(800, 600))

        self.selected_component = Selection(None)
        
        self.menubar = Menubar(self)
        self.config(menu=self.menubar)
        
        self.make_support_frames()
        self.add_interface()

        self.initialize_canvas_area()

        self.initialize_component_selection()
        self.initialize_canvas_selection()

        self.add_view()

        self.graph_saver = GraphSaver()
        self.view_saver = ViewSaver(self.graph_saver)

        self.graph_loader = GraphLoader(self.module_importer)
        self.view_loader = ViewLoader(self.graph_loader, self.module_manager, self.identifier_factory)

        self.file_interface = FileInterface()


    def make_support_frames(self):
        self.left_frame = tk.Frame(self, background="blue")
        self.right_frame = tk.Frame(self, background="green")

        self.right_frame.pack(side=tk.RIGHT, expand=False, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.left_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, pady=0, padx=0, anchor="ne")

    def add_interface(self):
        self.toolbox = Toolbox(self.right_frame)
        self.description_panel = DescriptionPanel(self.right_frame)

        self.description_panel.pack(side=tk.BOTTOM, expand=False, fill=tk.X, pady=0, padx=0, anchor="s")
        self.toolbox.pack(side=tk.BOTTOM, expand=True, fill=tk.Y, pady=0, padx=0, anchor="n")

    def initialize_canvas_selection(self):
        self.selected_canvas = Selection(None)
        self.selected_canvas.set_watcher(self.toolbox.canvas_selection_changed) 
        
        def tabChangedEvent(event):
            new_canvas_idx = event.widget.index("current")
            new_canvas = self.canvases[new_canvas_idx]
            self.selected_canvas.change(new_canvas)

        self.note.bind_all("<<NotebookTabChanged>>", tabChangedEvent)

    def initialize_component_selection(self):
        self.selected_component = Selection(None, properties = {'is_toolbox':False})

        self.toolbox.selected_component = self.selected_component
        self.description_panel.selected_component = self.selected_component

        self.selected_component.set_watcher(self.description_panel.component_selection_changed) 
        

    def predict_selection(self):
        graph = self.selected_canvas.get().get_selected_graph()
        runner = GraphRunner()
        print(runner.run(graph, {}))

    def compile_selection(self):
        print("Compiling functions...")
        graph = self.experiment_canvas.get_selected_graph()

        c = Compiler(GraphCompiler())
        c.compile(graph, "out.py")

        print("done")

    def save_current_view(self):
        pass

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


    def initialize_canvas_area(self):
        self.note = ttk.Notebook(self.left_frame)

        self.module_importer = ModuleImporter()
        self.module_manager = ModuleManager(self.module_importer)
        self.identifier_factory = IdentifierFactory()

        self.note.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor="nw")


        #TODO: Awaiting tests, refactor
        '''
        actual_agent_view = View("agent", self.module_manager, self.identifier_factory)
        actual_experiment_view = View("experiment", self.module_manager, self.identifier_factory)
        
        self.agent_canvas = DrawableCanvas(self.note, actual_agent_view)
        self.experiment_canvas = DrawableCanvas(self.note, actual_experiment_view)

        self.note.add(self.agent_canvas, text="Agents")
        self.note.add(self.experiment_canvas, text="Experiment")
        '''


    def add_view(self, view_name=None):
        if view_name is None:
            view_name = self.identifier_factory.get_next_identifier(name_string="view")

        view = View(view_name, self.module_manager, self.identifier_factory)
        self.process_view_in_ui(view)

        self.module_manager.register_view(view)

    def process_view_in_ui(self, view):
        canvas = DrawableCanvas(self.note, view)
        self.note.add(canvas, text=view.name)
        self.canvases.append(canvas)
        self.selected_canvas.change(canvas)
        canvas.selected_ui_element = self.selected_component
        self.note.select(len(self.canvases) - 1)

    def layout(self):
        self.description_panel.pack(side=tk.BOTTOM, expand=False, pady=0, padx=0, anchor="se")
        self.toolbox.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.note.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, pady=0, padx=0, anchor="ne")
