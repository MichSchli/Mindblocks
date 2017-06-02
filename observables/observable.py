class Observable:

    observers = None

    def __init__(self):
        self.observers = []

    def set_observer(self, observer_method):
        self.observers.append(observer_method)

    def notify_observers(self, properties=None):
        if properties is not None:
            for k in properties:
                self.properties[k] = properties[k]

        for oberver in self.observers:
            oberver(self)