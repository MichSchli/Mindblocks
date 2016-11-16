import imp

abstract = imp.load_source('abstract','interface/drawable_canvas.py')

class DatasetCanvas(abstract.DrawableCanvas):

    color="green"
