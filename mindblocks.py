import imp
import os

os.environ["THEANO_FLAGS"] = "floatX=float32,warn_float64=raise"

ui = imp.load_source('ui', 'interface/main.py')
interface = ui.Interface()
interface.mainloop()

