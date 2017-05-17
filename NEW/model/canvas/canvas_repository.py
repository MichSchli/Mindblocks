from NEW.model.canvas.canvas_model import CanvasModel
from NEW.observer.observable_dictionary import ObservableDict


class CanvasRepository:

    defined_canvases = None

    def __init__(self, identifier_factory):
        self.identifier_factory = identifier_factory
        self.defined_canvases = ObservableDict()

    def create_canvas(self):
        identifier = self.identifier_factory.get_next_identifier(name_string='canvas')
        canvas = CanvasModel(identifier)
        self.defined_canvases.append(canvas)
        return canvas
