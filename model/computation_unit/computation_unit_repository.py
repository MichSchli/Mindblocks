from observables.observable_dictionary import ObservableDict


class ComputationUnitRepository:

    computation_units = None
    identifier_factory = None

    def __init__(self, identifier_factory):
        self.computation_units = ObservableDict()
        self.identifier_factory = identifier_factory

    def create(self, computation_unit_model):
        identifier = self.identifier_factory.get_next_identifier(name_string='computation_unit')
        computation_unit_model.set_unique_identifier(identifier)

        self.computation_units.append(computation_unit_model)

    def get(self, computation_unit_specifications):
        models = []
        for model in self.computation_units.get_elements():
            if computation_unit_specifications.matches(model):
                models.append(model)
        return models
