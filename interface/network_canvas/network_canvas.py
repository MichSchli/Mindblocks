import imp

abstract = imp.load_source('abstract','interface/drawable_canvas.py')

class NetworkCanvas(abstract.DrawableCanvas):

    color="blue"
