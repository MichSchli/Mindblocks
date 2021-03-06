from interface.graphics.graphic import PlaceholderGraphic
from model.computation_unit.computation_unit_model import ComputationUnitModel
from model.identifiables.identifiable import Identifiable


class ToolboxItemModel(Identifiable):

    name = None
    prototype_class = None
    attributes = None
    package = None

    def get_name(self):
        return self.name

    def get_package(self):
        return self.package

    def get_attributes(self):
        return self.attributes

    def get_unique_identifier(self):
        return "Toolbox:"+self.package + "," + self.name

    def create_computation_model(self):
        return ComputationUnitModel()


