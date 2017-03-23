class Visitor:

    def run_visit(self, graph, function, arguments={}):
        for vertex in graph.topological_walk():
            function(vertex, arguments=arguments)

    def yield_visit(self, graph, function, arguments={}):
        for vertex in graph.topological_walk():
            for line in function(vertex, arguments=arguments):
                yield line

