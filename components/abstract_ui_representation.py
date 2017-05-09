from interface.graphics.graphic import *


class UIRepresentation:

    position = None

    def __init__(self, component, graphic):
        self.graphic = graphic
        self.component = component

    def get_graphic(self):
        return self.graphic

    def get_position(self):
        return self.component.get_position()

    def set_position(self, x, y):
        self.component.set_position(x, y)

    def draw(self, canvas):
        self.get_graphic().draw(canvas, self.get_position())

    def link_to(self, other):
        return Link(self, other)


class Link(UIRepresentation):

    def __init__(self, from_element, to_element):
        self.from_element = from_element
        self.to_element = to_element

    def draw(self, canvas):
        self.get_graphic().draw(canvas)

    def get_graphic(self):
        return EdgeLine(self.from_element, self.to_element)