import theano

class Graph():

    nodes = []
    
    def __init__(self):
        pass

    def add_node(self, node):
        self.nodes.append(node)

    def predict(self):
        inputs, outputs, parameters = self.compile()
        fn = theano.function(inputs=inputs, outputs=outputs)
        print(fn())
        exit()

    def compile(self):
        inputs = []
        outputs = []
        parameters = []

        for node in self.topological_walk():
            node.compile_theano()
            inputs.extend(node.inputs())
            outputs.extend(node.outputs())
            parameters.extend(node.parameters())


        return inputs, outputs, parameters 

              
    def topological_walk(self):
        S = [node for node in self.nodes if node.in_degree() == 0]

        while len(S) > 0:
            next_node = S.pop()

            # Propagate forward in the graph:
            for out_link in next_node.get_links_out():
                out_link.mark_satisfied(True)
                for end_node in out_link.get_partner_nodes():
                    if end_node.is_satisfied():
                        S.append(end_node)

            yield next_node

        # Prepare for next traversal:
        for node in self.nodes:
            for out_link in node.get_links_out():
                out_link.mark_satisfied(False)
        
class Link():

    def __init__(self):
        pass


class InLink(Link):

    partner = None
    
    def __init__(self, node):
        self.to_node = node

    def put(self, out_link):
        self.partner = out_link

    def get_value(self):
        return self.partner.value
        
class OutLink(Link):

    partners = []
    value = None
    satisfied = False
    
    def __init__(self, node):
        self.from_node = node

    def mark_satisfied(self, boolean):
        self.satisfied = boolean
        
    def put(self, in_link):
        self.partners.append(in_link)
        in_link.put(self)

    def set_value(self, value):
        self.value = value

    def get_partner_nodes(self):
        return [partner.to_node for partner in self.partners]
        
class Node():

    def __init__(self, links_in=0, links_out=0):
        self.links_in = [InLink(self) for _ in range(links_in)]
        self.links_out = [OutLink(self) for _ in range(links_out)]

    def get_links_in(self):
        return self.links_in

    def is_satisfied(self):
        for link in self.links_out:
            if link.satisfied == False:
                return False
        return True
    
    def in_degree(self):
        return len(self.links_in)

    def get_links_out(self):
        return self.links_out

    def compile_theano(self):
        pass

    def inputs(self):
        return []

    def outputs(self):
        return []

    def parameters(self):
        return []
    
class Constant(Node):
    
    def __init__(self, value):
        Node.__init__(self, links_out=1)
        self.value = value

    def compile_theano(self):
        self.links_out[0].set_value(theano.tensor.constant(self.value))

        
class Output(Node):

    def __init__(self):
        Node.__init__(self, links_in=1)

    def outputs(self):
        return [self.links_in[0].get_value()]

    
