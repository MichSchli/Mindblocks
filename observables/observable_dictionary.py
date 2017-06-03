from observables.observable import Observable
from observables.observed_event import ObservedEvent


class ObservableDict(Observable):

    elements = {}

    def __init__(self):
        Observable.__init__(self, events=['append', 'update', 'delete'])
        self.elements = {}

    '''
    Subscriber methods:
    '''

    def define_append_observer(self, observer):
        self.define_observer(observer, 'append')

    def define_update_observer(self, observer):
        self.define_observer(observer, 'update')

    def define_delete_observer(self, observer):
        self.define_observer(observer, 'delete')

    def define_change_observer(self, observer):
        self.define_observer(observer, 'append')
        self.define_observer(observer, 'update')
        self.define_observer(observer, 'delete')

    '''
    Event helpers:
    '''

    def handle_element_event(self, element, event_type):
        event = ObservedEvent(event_type)
        event.element = element
        self.notify_observers(event)

    '''
    Class methods:
    '''

    def append(self, element):
        self.elements[element.get_unique_identifier()] = element
        self.handle_element_event(element, 'append')

    def update(self, element):
        self.elements[element.get_unique_identifier()] = element
        self.handle_element_event(element, 'update')

    def delete(self, element):
        del self.elements[element.get_unique_identifier()]
        self.handle_element_event(element, 'delete')

    def as_list(self):
        return list(self.elements.items())

    def get(self, identifier):
        if identifier in self.elements:
            return self.elements[identifier]
        else:
            return None