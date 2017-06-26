from model.identifiables.identifiable import Identifiable


class ComputationUnitModel(Identifiable):
    """
    Model representing a single unit of computation. 
    To be compiled and included in a computational graph.
    """

    inputs = None
    outputs = None
    variables = None
    executable_function = None

    def __init__(self):
        self.define_inputs()
        self.define_outputs()
        self.define_variables()

        self.initialize_variables()

    def define_inputs(self):
        self.inputs = []

    def define_outputs(self):
        self.outputs = []

    def define_variables(self):
        self.variables = []

    def initialize_variables(self):
        self.variables = []

    def compile(self):
        pass
