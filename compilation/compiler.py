class Compiler:

    header_compiler = None
    graph_compiler = None

    def __init__(self, graph_compiler):
        self.graph_compiler = graph_compiler

    def compile(self, graph, output_file):
        output_file = open(output_file, 'w')

        self.write_section_header(output_file, "Imports")
        for line in self.graph_compiler.yield_headers(graph):
            print(line, file=output_file)
        print("", file=output_file)

        self.write_section_header(output_file, "Arguments")
        #self.write_arguments(graph, output_file)
        print("", file=output_file)

        self.write_section_header(output_file, "Code")
        for line in self.graph_compiler.yield_code(graph):
            print(line, file=output_file)
        print("", file=output_file)

        self.write_section_header(output_file, "Run")
        for line in self.graph_compiler.yield_run(graph):
            print(line, file=output_file)
        #self.write_output(graph, output_file)

        output_file.close()

    def write_arguments(self, graph, output_file):
        inputs = graph.get_inputs()

        print("import argparse", file=output_file)
        print("", file=output_file)
        print("""argument_parser = argparse.ArgumentParser(description="Generated mindblocks model.")""", file=output_file)
        #print("""argument_parser.add_argument("--mode", help="train/predict.", required=True)""", file=output_file)

        for inp in inputs:
            print("""argument_parser.add_argument("--p1", help="TBA.", required=True)""", file=output_file)

        print("args = argument_parser.parse_args()", file=output_file)

    def write_section_header(self, output_file, section):
        print("#=================================", file=output_file)
        print("# " + section + ":", file=output_file)
        print("#=================================", file=output_file)
        print("", file=output_file)

