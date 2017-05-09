import tkinter as tk

class Menubar(tk.Menu):

    def get_menus(self):
        return [
            ("File",
             [
                 ("New", self.placeholder),
                 ("Save", self.save),
                 ("Save View", self.placeholder),
                 ("Load", self.load),
                 ("Load View", self.placeholder),
                 ("Exit", self.quit_f)
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
                 ("Train", self.train),
                 ("Predict", self.predict),
                 ("Options", self.placeholder)
             ]
            ),
            ("Compile",
             [
                 ("Run", self.compile),
                 ("Options", self.placeholder)
             ]
            )
        ]

        
    
    def __init__(self, root):
        tk.Menu.__init__(self, root)
        self.root = root
        
        for menu in self.get_menus():
            self.__add_menu_from_list__(*menu)

    def placeholder(self):
        pass

    def save(self):
        self.root.save()

    def load(self):
        self.root.load()

    def quit_f(self):
        self.root.quit()

    def predict(self):
        self.root.predict_selection()

    def train(self):
        self.root.train_selection()

    def compile(self):
        self.root.compile_selection()
        
    def __add_menu_from_list__(self, title, l):
        menu = tk.Menu(self, tearoff=0)
        for k in l:
            menu.add_command(label=k[0], command=k[1])

        self.add_cascade(label=title, menu=menu)
            
