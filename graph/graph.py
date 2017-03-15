import theano

from graph.edge import Edge


class Graph:
    """
    Class representing a computational graph. The graph is a directed, tripartite tree, with vertices split into
    operations, input-links, and output-links.
    """

    vertices = None
    edges = None

    def __init__(self, vertex=None):
        if vertex is not None:
            self.vertices = [vertex]
        else:
            self.vertices = []

        self.edges = []

    def add_edge(self, u, v):
        edge = Edge(u, v)
        edge.set_graph(self)
        self.edges.append(edge)
        u.add_edge_out(edge)
        v.add_edge_in(edge)

    def add_vertex(self, v):
        self.vertices.append(v)

    def merge_and_link(self, u, v):
        if self == u.get_graph() and not self == v.get_graph():
            self.merge(v.get_graph())
        elif self == v.get_graph() and not self == u.get_graph():
            self.merge(u.get_graph())

        self.add_edge(u,v)

    def merge(self, other):
        for vertex in other.get_vertices():
            vertex.set_graph(self)

        for edge in other.get_edges():
            edge.set_graph(self)

        self.vertices.extend(other.get_vertices())
        self.edges.extend(other.get_edges())

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def compile_theano(self, mode='predict'):
        inputs, outputs, updates = self.build_theano_graph(mode)
        print(inputs, outputs, updates)
        fn = theano.function(inputs=inputs, outputs=outputs, updates=updates)
        return fn

    def run_python(self):
        yield """fn = graph.compile_theano(mode=args.mode)"""
        yield "fn()"

    def compile_python(self):
        yield "graph = Graph()"
        yield ""
        for line in self.build_python_graph():
            yield line

    def build_python_graph(self):
        for vertex in self.topological_walk():
            for line in vertex.python_init():
                if line is not None:
                    yield line

    def fetch_python_imports(self):
        for vertex in self.topological_walk():
            statement = vertex.get_python_import()
            if statement is not None:
                yield statement

    def compile_python_imports(self):
        yield "from graph.graph import Graph"
        imports = self.fetch_python_imports()
        for line in set(imports):
            yield line

    def get_inputs(self):
        inputs = []
        for vertex in self.topological_walk():
            inputs.extend(vertex.theano_inputs())
        return inputs

    def build_theano_graph(self, mode):
        inputs = []
        outputs = []
        updates = []

        for vertex in self.topological_walk():
            print(vertex)
            print(vertex.get_name())
            print(vertex.parse_attributes())
            vertex.compile_theano()
            inputs.extend(vertex.theano_inputs())
            outputs.extend(vertex.theano_outputs())
            updates.extend(vertex.theano_updates())

        return inputs, outputs, updates

    def topological_walk(self):
        S = [vertex for vertex in self.vertices if vertex.in_degree() == 0]

        for edge in self.edges:
            print(edge)
            print(edge.origin)
            print(edge.destination)

        print(self.vertices[0].get_edges_out())

        while len(S) > 0:
            next_vertex = S.pop()

            # Propagate forward in the graph:
            for out_edge in next_vertex.get_edges_out():
                print("HAHAHAH")
                print(out_edge.get_destination())
                out_edge.mark_satisfied(True)
                if out_edge.get_destination().is_satisfied():
                    S.append(out_edge.get_destination())

                print(out_edge)

            yield next_vertex

        # Prepare for next traversal:
        for vertex in self.vertices:
            for out_edge in vertex.get_edges_out():
                out_edge.mark_satisfied(False)
