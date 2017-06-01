from NEW.model.canvas.canvas_model import CanvasModel
from NEW.observer.observable_dictionary import ObservableDict


class CanvasRepository:

    defined_canvases = None
    graph_repository = None
    xml_helper = None

    def __init__(self, identifier_factory, graph_repository, xml_helper):
        self.identifier_factory = identifier_factory
        self.graph_repository = graph_repository
        self.xml_helper = xml_helper
        self.defined_canvases = ObservableDict()

    def create_canvas(self):
        identifier = self.identifier_factory.get_next_identifier(name_string='canvas')
        canvas = CanvasModel(identifier)
        self.defined_canvases.append(canvas)
        return canvas

    def update_canvas(self, canvas):
        self.defined_canvases.update(canvas)

    def save_canvas(self, canvas, outfile):
        name = canvas.get_unique_identifier()

        print(self.xml_helper.get_header("view", {"name": name}), file=outfile)
        for graph in canvas.get_defined_graphs():
            self.graph_repository.save_graph(graph, outfile)
        print(self.xml_helper.get_footer("view"), file=outfile)
