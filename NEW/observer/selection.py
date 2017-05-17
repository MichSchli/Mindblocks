from NEW.observer.observable import Observable


class Selection(Observable):

    element = None
    properties = None

    def __init__(self, element, properties=None):
        self.element = element
        self.properties = properties

        Observable.__init__(self)

    def get(self):
        return self.element

    def change(self, element, properties=None):
        self.element = element
        self.notify_observers(properties=properties)


