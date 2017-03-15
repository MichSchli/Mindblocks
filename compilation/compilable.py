class Compilable:

    def generate_code(self):
        yield self.get_name() + " = " +  self.__class__.__name__ + "()"
        yield "graph.merge(" + self.get_name() + ".get_graph())"
        if self.attributes != {}:
            yield self.get_name() + ".attributes = " + str(self.attributes)
        for enumerator, in_edge in enumerate(self.edges_in):
            yield in_edge.origin.get_name() + " = " + self.get_name() + ".edges_in[" + str(enumerator) + "].origin"
        for enumerator, out_edge in enumerate(self.edges_out):
            yield out_edge.destination.get_name() + " = " + self.get_name() + ".edges_out[" + str(enumerator) + "].destination"

        for in_edge in self.edges_in:
            in_link = in_edge.origin
            for x in in_link.edges_in:
                yield "graph.add_edge(" + x.origin.get_name() + ", " + in_link.get_name() + ")"
        yield ""

    def get_imports(self):
        return "from " + self.module + " import " + self.__class__.__name__