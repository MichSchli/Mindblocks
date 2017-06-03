from observables.observable import Observable
from observables.observed_event import ObservedEvent


class Selection(Observable):

    element = None
    properties = None

    def __init__(self, element):
        self.element = element

        Observable.__init__(self, events=['selection_changed'])

    def get(self):
        return self.element

    def change(self, element):
        event = ObservedEvent('selection_changed')
        event.new_element = element
        event.old_element = self.element

        self.element = element
        self.notify_observers(event)


