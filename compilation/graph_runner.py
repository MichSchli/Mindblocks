from graph.visitor import Visitor


class GraphRunner(Visitor):

    def __run_vertex__(self, vertex, arguments={}):
        vertex.parse_attributes()
        vertex.compile_python()

    def run(self, graph):
        self.run_visit(graph, self.__run_vertex__)