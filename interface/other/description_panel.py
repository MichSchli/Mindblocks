import tkinter as tk
import numpy as np

class DescriptionPanel(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=200, width=200, background='white')

        self.title = DescriptionTitle(self)
        self.box = DescriptionBox(self)
        
        self.title.pack(side=tk.TOP, expand=False, fill=tk.X, pady=0, padx=0, anchor="ne")
        self.box.scrollbar.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        #self.box.text_field.pack()
        self.box.text_field.pack(side=tk.LEFT, expand=True, fill=tk.Y)
        self.box.pack(side=tk.TOP, expand=False, fill=tk.BOTH, pady=0, padx=0, anchor="ne")

    def component_selection_changed(self, selection):
        self.title.change(selection.get())
        self.box.change(selection.get())


class DescriptionTitle(tk.Frame):

    max_length = 20
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=30)

        self.text = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.text)
        self.label.pack()
        #self.text.pack(side=tk.TOP, expand=False, fill=tk.X)

    def change(self, component):
        if component is None:
            title = "<No selection>"
        else:
            title = component.get_name()

        if len(title) > self.max_length:
            title = title[:self.max_length]+"..."
            
        self.text.set(title)
        
class DescriptionBox(tk.Frame):

    component = None

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=160, width=200)

        self.scrollbar = tk.Scrollbar(self)
        # textfield resizing seems to be broken, so I hardcoded the size
        self.text_field = tk.Text(self, yscrollcommand=self.scrollbar.set, width=29, height=15)


        self.text_field.bind('<KeyRelease>', self.wrote_change)

        self.scrollbar.config(command=self.text_field.yview)

    def wrote_change(self, event):
        parse = self.try_parse()
        if parse is not None:
            self.component.attributes = parse

    def try_parse(self):
        lines = self.text_field.get(1.0, tk.END).strip().split('\n')
        lines = [l.split('=') for l in lines]

        for line in lines:
            if len(line) != 2 or len(line[1])==0:
                return None

        d = {}
        for line in lines:
            parsed = self.parse_field(line[1])
            if parsed is None:
                return None

            d[line[0]] = parsed

        return d

    def parse_field(self, string):
        return string

    def change(self, component):
        self.component = component
        self.text_field.delete(1.0, tk.END)
        if component is not None:
            for attribute in component.attributes:
                self.text_field.insert(tk.END, attribute+"="+str(component.attributes[attribute])+'\n')
