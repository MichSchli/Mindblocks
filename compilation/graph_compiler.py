from graph.visitor import Visitor


class GraphCompiler(Visitor):

    def __yield_vertex_header__(self, vertex, arguments={}):
        for imp in vertex.get_python_import():
            if imp:
                yield imp

    def __yield_vertex_code__(self, vertex, arguments={}):
        for line in vertex.python_init(arguments=arguments):
            if line:
                yield line

    def yield_headers(self, graph):
        yield "from graph.graph import Graph"
        yield "from compilation.graph_runner import GraphRunner"
        for line in self.yield_visit(graph, self.__yield_vertex_header__):
            yield line

    def yield_code(self, graph, name=None):
        if name is None:
            name = "graph"
        yield name + " = Graph()"
        yield ""
        for line in self.yield_visit(graph, self.__yield_vertex_code__, arguments={'name':name}):
            yield line

    def yield_run(self, graph):
        yield "runner = GraphRunner()"
        yield "runner.run(graph)"
