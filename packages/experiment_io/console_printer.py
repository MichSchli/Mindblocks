from NEW.model.component.component_model import ComponentModel

class ConsolePrinter(ComponentModel):

    name = "ConsolePrinter"
    default_in_sockets = [{'position': [0, 20],
                 'name': 'Input'}]

    attributes = {}

    def compile_python(self):
        to_be_output = self.pull_by_index(0)

        print(to_be_output)


