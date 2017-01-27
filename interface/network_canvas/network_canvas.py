from importer.importer import Importer
from interface.drawable_canvas import DrawableCanvas


class NetworkCanvas(DrawableCanvas):

    def __init__(self, parent):
        DrawableCanvas.__init__(self, parent)

        importer = Importer()
        modules = importer.import_modules()
        self.available_modules = modules

    available_modules = None
