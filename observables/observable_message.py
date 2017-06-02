from observables.observable import Observable

class ObservableMessage(Observable):

    message = None

    def __init__(self):
        Observable.__init__(self)
        self.elements = []

    def update(self, message):
        self.message = message
        self.notify_observers()