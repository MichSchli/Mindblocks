from interface.graphics.graphic import PlaceholderGraphic


class ToolboxItemModel:

    name = None
    prototype_class = None
    attributes = None

    # TODO: Placeholder until graphics updated. Model should not reference view.
    def instantiate_graphic(self):
        return PlaceholderGraphic(self.get_name())

    def get_name(self):
        return self.name

    def get_attributes(self):
        return self.attributes

