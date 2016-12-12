class Selection():

    element = None
    properties = None
    watchers = None

    def __init__(self, element, properties=None):
        self.element = element
        self.properties = properties
        self.watchers = []
        

    def get(self):
        return self.element

    def change(self, element, properties=None):
        self.element = element

        if properties is not None:
            for k in properties:
                self.properties[k] = properties[k]

        for watcher in self.watchers:
            watcher(self)

    def set_watcher(self, watcher_method):
        self.watchers.append(watcher_method)
