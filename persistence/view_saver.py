from persistence.XmlProducer import XmlProducer

class ViewSaver(XmlProducer):

    graph_saver = None

    def __init__(self, graph_saver):
        self.graph_saver = graph_saver

    def process(self, view):
        name = view.name

        yield self.get_header("view", {"name":name})
        for graph in view.get_defined_graphs():
            for line in self.graph_saver.process(graph):
                yield line
        yield self.get_footer("view")
