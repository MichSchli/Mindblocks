import imp

components = imp.load_source('graphics','components/component.py')
abstract = imp.load_source('abstract','interface/drawable_canvas.py')

class OptimizerCanvas(abstract.DrawableCanvas):

    available_components=[components.Placeholder("o1")]
