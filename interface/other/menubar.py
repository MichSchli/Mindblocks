import tkinter as tk

from observables.observable import Observable
from observables.observable_message import ObservableMessage
from observables.observed_event import ObservedEvent


class Menubar(tk.Menu, Observable):

    def get_menus(self):
        return [
            ("File",
             [
                 ("New", self.placeholder),
                 ("Save", self.open_save_dialog_and_cause_event),
                 ("Load", self.open_load_dialog_and_cause_event),
                 ("Exit", self.placeholder)
             ]
            ),
            ("View",
             [
                 ("Add view", self.cause_event),
                 ("Save view", self.open_save_dialog_and_cause_event),
                 ("Load view", self.open_load_dialog_and_cause_event),
                 ("Save view as module", self.placeholder),
             ]
             ),
            ("Edit",
             [
                 ("Undo", self.placeholder),
                 ("Redo", self.placeholder),
                 ("Cut", self.placeholder),
                 ("Copy", self.placeholder),
                 ("Paste", self.placeholder)
             ]
            ),
            ("Run",
             [
                 ("Train", self.placeholder),
                 ("Predict", self.placeholder),
                 ("Options", self.placeholder)
             ]
            )
        ]

    def __init__(self, root, file_interface):
        tk.Menu.__init__(self, root)
        self.root = root
        self.file_interface = file_interface
        
        for menu in self.get_menus():
            self.__add_menu_from_list__(*menu)

        events = []
        for root,options in self.get_menus():
            for option in options:
                events.append(root+":"+option[0])

        Observable.__init__(self, events=events)

    def placeholder(self, event_name):
        return lambda: print(event_name)

    def cause_event(self, event_name):
        def inner_cause():
            event = ObservedEvent(event_name)
            self.notify_observers(event)
        return inner_cause

    def open_save_dialog_and_cause_event(self, event_name):
        def inner_cause():
            event = ObservedEvent(event_name)
            event.save_file = self.file_interface.save_as_file()
            self.notify_observers(event)
        return inner_cause

    def open_load_dialog_and_cause_event(self, event_name):
        def inner_cause():
            event = ObservedEvent(event_name)
            event.load_file = self.file_interface.load_file()
            self.notify_observers(event)
        return inner_cause

    def define_add_view_observer(self, observer):
        self.define_observer(observer, "View:Add view")

    def define_save_selected_canvas_observer(self, observer):
        self.define_observer(observer, "View:Save view")

    def define_load_single_canvas_observer(self, observer):
        self.define_observer(observer, "View:Load view")

    def define_save_all_observer(self, observer):
        self.define_observer(observer, "File:Save")

    def define_load_all_observer(self, observer):
        self.define_observer(observer, "File:Load")
        
    def __add_menu_from_list__(self, root, options):
        menu = tk.Menu(self, tearoff=0)

        for option in options:
            event_name = root+":"+option[0]
            menu.add_command(label=option[0], command=option[1](event_name))

        self.add_cascade(label=root, menu=menu)
