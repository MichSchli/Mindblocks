class Observable:

    observers = None

    def __init__(self, events=[]):
        if events:
            self.observers = {k:[] for k in events}
        else:
            self.observers = {'default':[]}


    def define_observer(self, observer_method, event='default'):
        self.observers[event].append(observer_method)

    def notify_observers(self, event):
        observer_list = self.observers[event.event_type]
        for oberver in observer_list:
            oberver(event)