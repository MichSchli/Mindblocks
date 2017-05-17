from graph.graph_runners.theano_graph_runner import TheanoGraphRunner

from compilation.graph_compiler import GraphCompiler
from components.abstract_component import Component


class SubgraphComponent(Component):
    name = "Subgraph"
    default_out_sockets = []
    default_in_sockets = []

    def python_init(self, arguments={}):
        # Define the subgraph
        # Or later: Mark for definition
        gc = GraphCompiler()
        for line in gc.yield_code(self.sub_graph, name="subgraph"):
            yield line

        yield "manifest = " + str(self.manifest)
        yield self.get_name() + " = " + self.__class__.__name__ + "(subgraph, manifest=manifest)"
        yield arguments['name'] + ".merge(" + self.get_name() + ".get_graph())"
        if self.attributes != {}:
            yield self.get_name() + ".attributes = " + str(self.attributes)
        for enumerator, in_edge in enumerate(self.edges_in):
            yield in_edge.origin.get_name() + " = " + self.get_name() + ".edges_in[" + str(enumerator) + "].origin"
        for enumerator, out_edge in enumerate(self.edges_out):
            yield out_edge.destination.get_name() + " = " + self.get_name() + ".edges_out[" + str(
                enumerator) + "].destination"

        for in_edge in self.edges_in:
            in_link = in_edge.origin
            for x in in_link.edges_in:
                yield arguments['name'] + ".add_edge(" + x.origin.get_name() + ", " + in_link.get_name() + ")"
        yield ""

    def get_python_import(self):
        yield "from " + self.module + " import " + self.__class__.__name__
        gc = GraphCompiler()
        for line in gc.yield_headers(self.sub_graph):
            yield line

    def compile_theano(self):
        pass

    def compile_python(self):
        input_d = {}
        for i in range(len(self.inputs)):
            input_d[self.inputs[i]] = self.pull_by_index(i)

        output_d = self.graph_runner.run(self.sub_graph, input_d)

        for i in range(len(self.outputs)):
            self.push_by_index(i, output_d[self.outputs[i]])


    def __init__(self, manifest=None, identifier=None):
        self.graph_runner = TheanoGraphRunner()
        Component.__init__(self, manifest=manifest, identifier=identifier)



    def update_attributes(self, new_attributes):
        Component.update_attributes(self, new_attributes)

        target_view = self.attributes['target_view']
        target_graph = self.attributes['target_graph']

        self.subgraph = self.view_manager.get_graph(target_view, target_graph)

        self.inputs = [i[0] for i in self.sub_graph.get_inputs()]
        self.outputs = [o[0] for o in self.sub_graph.get_outputs()]

        self.default_in_sockets = []
        self.default_out_sockets = []

        available_space = 80
        if len(self.inputs) > 0:
            input_spacing = available_space/(len(self.inputs))
            for i,inp in enumerate(self.inputs):
                self.default_in_sockets.append({'position': [-40 + int((i+0.5) * input_spacing), 20],
                                      'name': inp})

        if len(self.outputs) > 0:
            output_spacing = available_space/(len(self.outputs))
            for i,oup in enumerate(self.outputs):
                self.default_out_sockets.append({'position': [-40 + int((i+0.5) * output_spacing), -20],
                                      'name': oup})




    def copy(self, identifier=None):
        return self.__class__(self.graph, identifier=identifier)
