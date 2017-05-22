import theano.tensor as T

class GraphInput:

    name = None
    var_dim = None
    var_type = None
    variable = None

    def __init__(self, name, dim, type="float32"):
        self.name = name
        self.var_dim = dim
        self.var_type=type

    def compile_theano(self):
        b = tuple([False for _ in self.var_dim])
        self.variable = T.TensorType(dtype=self.var_type, broadcastable=b)(self.name)
        return self.variable