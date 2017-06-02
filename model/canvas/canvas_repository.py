from model.canvas.canvas_model import CanvasModel
from observables.observable_dictionary import ObservableDict


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

    def load_canvases(self, infile):
        lines = infile.read()
        canvases = []
        index = 0
        while len(lines) -1 > index:
            canvas, index = self.load_next_canvas(lines, start_index=index)
            canvases.append(canvas)
            self.defined_canvases.append(canvas)

        return canvases

    def load_next_canvas(self, lines, start_index=0):
        symbol, attributes, next_index = self.xml_helper.pop_symbol(lines, start_index=start_index)
        name = attributes["name"]

        canvas = CanvasModel(name)

        symbol, attributes, _ = self.xml_helper.pop_symbol(lines, start_index=next_index)
        while symbol != "/view":
            graph, next_index = self.graph_repository.load_next_graph(lines, start_index=next_index)
            canvas.append_graph(graph)
            symbol, attributes, _ = self.xml_helper.pop_symbol(lines, start_index=next_index)
            print(symbol)

        self.update_canvas(canvas)

        symbol, attributes, next_index = self.xml_helper.pop_symbol(lines, start_index=next_index)
        return canvas, next_index
