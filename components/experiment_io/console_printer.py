from components.component import Component

class ConsolePrinter(Component):

    name = "ConsolePrinter"
    links_in = [{'position': [0,20],
                 'name': 'Input'}]

    attributes = {}

    def compile_python(self):
        to_be_output = self.pull_by_index(0)

        print(to_be_output)


