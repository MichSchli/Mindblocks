class GraphPrototypeSpecifications:

    identifier = None
    graph_identifier = None

    def matches(self, prototype):
        if self.identifier is not None and self.identifier != prototype.get_unique_identifier():
            return False

        if self.graph_identifier is not None and self.graph_identifier != prototype.graph_identifier:
            return False

        return True