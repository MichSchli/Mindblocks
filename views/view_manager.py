from views.view import View


class ViewManager:

    views = {}

    def __init__(self, identifier_factory, component_factory):
        self.views = {}
        self.identifier_factory = identifier_factory
        self.component_factory = component_factory

    def create_view(self, view_name=None):
        if view_name is None:
            view_name = self.identifier_factory.get_next_identifier(name_string="view")

        view = View(view_name, self.identifier_factory)
        self.add_view_with_name(view_name, view)
        return view

    def add_view(self, view):
        self.add_view_with_name(view.name, view)

    def add_view_with_name(self, name, view):
        self.views[name] = view

    def get_view(self, name):
        return self.views[name]

    def get_graph(self, view_name, graph_name):
        view = self.get_view(view_name)
        graph = view.get_graph(graph_name)
        return graph