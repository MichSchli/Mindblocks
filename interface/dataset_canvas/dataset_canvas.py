import imp

components = imp.load_source('graphics','components/component.py')
abstract = imp.load_source('abstract','interface/drawable_canvas.py')

class DatasetCanvas(abstract.DrawableCanvas):

    available_components = [components.Placeholder("d1"), components.Placeholder("d2"), components.Placeholder("d3")]
