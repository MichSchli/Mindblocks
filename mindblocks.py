import imp

ui = imp.load_source('ui', 'interface/main.py')
interface = ui.Interface()
interface.mainloop()

