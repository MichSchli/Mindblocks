class ComputationUnitSpecification:

    identifiers = None

    def __init__(self):
        self.identifiers = []

    def matches(self, computation_unit_model):
        if computation_unit_model.get_unique_idetifier() not in self.identifiers:
            return False
        return True
