from persistence.XmlReader import XmlReader
from views.view import View


class ViewLoader(XmlReader):

    def __init__(self, graph_loader, module_manager, identifier_factory):
        self.graph_loader = graph_loader
        self.module_manager = module_manager
        self.identifier_factory = identifier_factory

    def load_next_view(self, lines, start_index=0):
        symbol, attributes, next_index = self.pop_symbol(lines, start_index=start_index)
        name = attributes["name"]

        view = View(name, self.module_manager, self.identifier_factory)

        symbol, attributes, _ = self.pop_symbol(lines, start_index=next_index)
        while symbol != "/view":
            graph, next_index = self.graph_loader.load_next_graph(lines, start_index=next_index)
            view.append_graph(graph)
            symbol, attributes, _ = self.pop_symbol(lines, start_index=next_index)

        return view


