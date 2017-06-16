class PrototypeSpecifications:

    package = None
    name = None
    identifier = None

    def matches(self, prototype):
        if self.package is not None and prototype.get_package() != self.package:
            return False

        if self.name is not None and prototype.get_name() != self.name:
            return False

        if self.identifier is not None and prototype.get_identifier() != self.identifier:
            return False

        return True
