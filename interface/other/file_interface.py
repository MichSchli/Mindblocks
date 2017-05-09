from tkinter import filedialog

class FileInterface:

    def save_as_file(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".mb")

        return f

    def load_file(self):
        f = filedialog.askopenfile(mode='r')

        return f
