import imp
graphics = imp.load_source('graphics','interface/graphics/graphic.py')

abstract = imp.load_source('abstract','interface/drawable_canvas.py')

class NetworkCanvas(abstract.DrawableCanvas):

    available_components = [graphics.Placeholder("n1"), graphics.Placeholder("n2")]
