import imp
graphics = imp.load_source('graphics','interface/graphics/graphic.py')

abstract = imp.load_source('abstract','interface/drawable_canvas.py')

class DatasetCanvas(abstract.DrawableCanvas):

    available_components = [graphics.Placeholder("d1"), graphics.Placeholder("d2"), graphics.Placeholder("d3")]
