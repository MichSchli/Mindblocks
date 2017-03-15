class Compiler:

    def compile(self, graph, output_file):
        output_file = open(output_file, 'w')

        self.write_section_header(output_file, "Imports")
        self.write_imports(graph, output_file)
        print("", file=output_file)

        self.write_section_header(output_file, "Arguments")
        self.write_arguments(graph, output_file)
        print("", file=output_file)

        self.write_section_header(output_file, "Code")
        self.write_graph(graph, output_file)
        print("", file=output_file)

        self.write_section_header(output_file, "Run")
        self.write_output(graph, output_file)

        output_file.close()

    def write_arguments(self, graph, output_file):
        inputs = graph.get_inputs()

        print("import argparse", file=output_file)
        print("", file=output_file)
        print("""argument_parser = argparse.ArgumentParser(description="Generated mindblocks model.")""", file=output_file)
        print("""argument_parser.add_argument("--mode", help="train/predict.", required=True)""", file=output_file)

        for inp in inputs:
            print("""argument_parser.add_argument("--p1", help="TBA.", required=True)""", file=output_file)

        print("args = argument_parser.parse_args()", file=output_file)

    def write_section_header(self, output_file, section):
        print("#=================================", file=output_file)
        print("# " + section + ":", file=output_file)
        print("#=================================", file=output_file)
        print("", file=output_file)


class MindblocksCompiler(Compiler):

    def write_imports(self, graph, output_file):
        for line in graph.compile_python_imports():
            print(line, file=output_file)

    def write_graph(self, graph, output_file):
        for line in graph.compile_python():
            print(line, file=output_file)

    def write_output(self, graph, output_file):
        for line in graph.run_python():
            print(line, file=output_file)


