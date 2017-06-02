from observables.observable import Observable

class ObservableList(Observable):

    elements = []

    def __init__(self):
        Observable.__init__(self)
        self.elements = []

    def append(self, element):
        self.elements.append(element)
        self.notify_observers()

    def extend(self, elements):
        self.elements.extend(elements)
        self.notify_observers()