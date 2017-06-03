import tkinter as tk
from tkinter import ttk

from controller.mindblocks_controller import MindblocksController
from interface.drawable_canvas import DrawableCanvas
from interface.other.description_panel import DescriptionPanel
from interface.other.file_interface import FileInterface
from interface.other.menubar import Menubar
from interface.other.toolbox import Toolbox
from observables.observable import Observable
from observables.observed_event import ObservedEvent
from observables.selection import Selection


#from views.view_manager import ViewManager


class Interface(tk.Tk, Observable):

    drawables = []

    def __init__(self):
        tk.Tk.__init__(self)
        Observable.__init__(self, events=['clicked', 'tab_changed'])

        '''
        Initialize controller
        '''

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
        self.controller = MindblocksController(self)
        self.controller.update_toolbox()
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
        #self.description_panel.selected_component = self.selected_component
        #self.selected_component.define_observer(self.description_panel.component_selection_changed)
        self.description_panel.pack(side=tk.BOTTOM, expand=False, fill=tk.X, pady=0, padx=0, anchor="s")

    def display_modules(self, modules):
        self.toolbox.display_modules(modules)

    def initialize_toolbox(self):
        self.toolbox = Toolbox(self.right_frame)
        #self.toolbox.selected_component = self.selected_component
        #self.toolbox.display_modules(self.module_manager.fetch_basic_modules())
        self.toolbox.pack(side=tk.TOP, expand=True, fill=tk.Y, pady=0, padx=0, anchor="n")

    def initialize_canvas_area(self):
        self.note = ttk.Notebook(self.left_frame)
        self.note.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor="nw")

    def define_tab_changed_observer(self, event_handler):
        #Workaround to keep gui event in view
        def tabChangedEvent(e):
            text = self.note.tab(self.note.select(), "text")

            event = ObservedEvent('tab_changed')
            event.new_canvas_unique_identifier = text

            event_handler(event)

        self.note.bind_all("<<NotebookTabChanged>>", tabChangedEvent)

    def click(self, location, element):
        event = ObservedEvent('clicked')
        event.location = location
        event.element = element
        self.notify_observers(event)

    def define_click_observer(self, observer):
        self.define_observer(observer, event='clicked')

    def initialize_selectors(self):
        pass #self.selected_component = Selection(None, properties = {'is_toolbox':False})


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

    def save_current_view(self):
        canvas = self.selected_canvas.get()
        self.controller.save_single_canvas(canvas.view)

    def select_load_file(self):
        infile = self.file_interface.load_file()
        return infile

    def load_view(self):
        self.controller.load_all_canvases_from_file()

    def process_component_in_ui(self, component, location):
        self.selected_canvas.get().add_ui_component(component, location)

    def process_edge_in_ui(self, edge):
        self.selected_canvas.get().add_ui_edge(edge)

    def show_canvas(self, canvas):
        for i,tab in enumerate(self.note.tabs()):
            text = self.note.tab(tab, option="text")
            if text == canvas.get_unique_identifier():
                self.note.select(i)
                break

    def add_canvas(self, canvas):
        drawable = DrawableCanvas(self.note, canvas, self.controller, self)
        self.drawables.append(drawable)
        self.note.add(drawable, text=canvas.get_unique_identifier())

    def redraw_canvas(self, canvas):
        for i,tab in enumerate(self.note.tabs()):
            text = self.note.tab(tab, option="text")
            if text == canvas.get_unique_identifier():
                self.drawables[i].replace_view(canvas)
