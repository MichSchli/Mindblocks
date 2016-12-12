import tkinter as tk

class DescriptionPanel(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=200, background='white')

        self.title = DescriptionTitle(self)
        self.box = DescriptionBox(self)
        
        self.title.pack(side=tk.TOP, expand=False, fill=tk.X, pady=0, padx=0, anchor="ne")
        self.box.pack(side=tk.TOP, expand=False, fill=tk.X, pady=0, padx=0, anchor="ne")



    def component_selection_changed(self, selection):
        self.title.change(selection.get())


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
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=160)
