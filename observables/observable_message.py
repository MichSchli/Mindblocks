from observables.observable import Observable
from observables.observed_event import ObservedEvent


class ObservableMessage(Observable):

    message = None

    def __init__(self):
        Observable.__init__(self)

    def update(self, message):
        event = ObservedEvent()
        event.message = message
        self.notify_observers(event)