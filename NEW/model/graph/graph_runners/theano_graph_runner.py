import theano

from NEW.model.graph.graph_runners.visitor import Visitor


class TheanoGraphRunner(Visitor):

    theano_function = None
    input_list = None
    output_list = None
    updates_list = None

    def __run_vertex__(self, vertex, arguments={}):
        vertex.parse_attributes()
        vertex.compile_theano()


    def __gather_inputs__(self, vertex, arguments={}):
        for elem in vertex.theano_inputs():
            yield elem

    def __gather_outputs__(self, vertex, arguments={}):
        for elem in vertex.theano_outputs():
            yield elem

    def __gather_updates__(self, vertex, arguments={}):
        for elem in vertex.theano_updates():
            yield elem


    def input_list_from_dictionary(self, input_dictionary):
        return [input_dictionary[entry[0]] for entry in self.input_list]

    def output_dictionary_from_list(self, output_list):
        d = {}
        for i in range(len(output_list)):
            d[self.output_list[i][0]] = output_list[i]
        return d

    def run(self, graph, input_dictionary):
        if self.theano_function is None:
            self.run_visit(graph, self.__run_vertex__)

            self.input_list = list(self.yield_visit(graph, self.__gather_inputs__))
            self.output_list = list(self.yield_visit(graph, self.__gather_outputs__))
            self.updates_list = list(self.yield_visit(graph, self.__gather_updates__))

            print(self.input_list)

            theano_inputs = [i[1] for i in self.input_list]
            theano_outputs = [i[1] for i in self.output_list]
            theano_updates = [i[1] for i in self.updates_list]

            self.theano_function = theano.function(inputs=theano_inputs, outputs=theano_outputs, updates=theano_updates)

        input_list = self.input_list_from_dictionary(input_dictionary)
        print(input_list)
        output_list = self.theano_function(input_list)

        return self.output_dictionary_from_list(output_list)