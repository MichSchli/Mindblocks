import imp

abstract = imp.load_source('abstract','interface/drawable_canvas.py')

class OptimizerCanvas(abstract.DrawableCanvas):

    color="red"
