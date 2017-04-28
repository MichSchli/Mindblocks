from graph.visitor import Visitor
from persistence.XmlProducer import XmlProducer


class GraphSaver(Visitor, XmlProducer):

    def __process_vertex__(self, vertex, arguments={}):
        name = vertex.get_unique_identifier()
        yield self.get_header("component", {"name":name}, indentation=2)

        if vertex.manifest is not None:
            yield self.get_header("class", indentation=3) + vertex.manifest['name'] + self.get_footer("class")
            yield self.get_header("package", indentation=3) + vertex.manifest['package'] + self.get_footer("package")

        for attribute in vertex.attributes:
            yield self.get_header("attribute", {"key":attribute}, indentation=3) + vertex.attributes[attribute] + self.get_footer("attribute")

        for edge in vertex.get_edges_in():
            sender_name = edge.get_origin().get_unique_identifier() + ":" + edge.get_out_socket_name()
            yield self.get_header("link", {"socket" : edge.get_in_socket_name()}, indentation=3) + sender_name + self.get_footer("link")

        yield self.get_footer("component", indentation=2)

    def process(self, graph):
        name = graph.get_unique_identifier()

        yield self.get_header("graph", {"name":name}, indentation=1)
        for line in self.yield_visit(graph, self.__process_vertex__):
            yield line
        yield self.get_footer("graph", indentation=1)
