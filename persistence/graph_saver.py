from graph.visitor import Visitor
from persistence.XmlProducer import XmlProducer


class GraphSaver(Visitor, XmlProducer):

    def __process_vertex__(self, vertex, arguments={}):
        if vertex.is_socket():
            return

        name = vertex.get_unique_identifier()
        yield self.get_header("component", {"name":name}, indentation=2)

        if vertex.manifest is not None:
            yield self.get_header("class", indentation=3) + vertex.manifest['name'] + self.get_footer("class")
            yield self.get_header("package", indentation=3) + vertex.manifest['package'] + self.get_footer("package")

        for attribute in vertex.attributes:
            yield self.get_header("attribute", {"key":attribute}, indentation=3) + vertex.attributes[attribute] + self.get_footer("attribute")

        for edge in vertex.get_edges_in():
            in_socket = edge.get_origin()
            if in_socket.is_socket():
                out_socket_names = [e.origin.get_unique_identifier() for e in in_socket.get_edges_in()]
                if out_socket_names:
                    in_socket_name = in_socket.description['name']
                    socket_string = self.get_header("socket", {"name": in_socket_name}, indentation=3)
                    socket_string += ",".join(out_socket_names)
                    socket_string += self.get_footer("socket")
                    yield socket_string

        yield self.get_footer("component", indentation=2)

    def process(self, graph):
        name = graph.get_unique_identifier()

        yield self.get_header("graph", {"name":name}, indentation=1)
        for line in self.yield_visit(graph, self.__process_vertex__):
            yield line
        yield self.get_footer("graph", indentation=1)
