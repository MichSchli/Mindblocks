from observables.observable import Observable

class ObservableDict(Observable):

    elements = {}

    def __init__(self):
        Observable.__init__(self)
        self.elements = {}

    def append(self, element):
        self.elements[element.get_unique_identifier()] = element
        self.notify_observers()

    def update(self, element):
        self.elements[element.get_unique_identifier()] = element
        self.notify_observers()

    def delete(self, element):
        del self.elements[element.get_unique_identifier()]
        self.notify_observers()

    def as_list(self):
        return list(self.elements.items())

    def get(self, identifier):
        if identifier in self.elements:
            return self.elements[identifier]
        else:
            return None