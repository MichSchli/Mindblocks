import unittest

from module_management.module_importer import ModuleImporter
from persistence.graph_loader import GraphLoader

class GraphSaverTest(unittest.TestCase):

    def setUp(self):
        self.module_importer = ModuleImporter()
        self.graph_loader = GraphLoader(self.module_importer)

    def tearDown(self):
        self.graph_saver = None


    def testLoadEmptyGraph(self):
        lines = "<graph name=TestGraph>" \
                + "</graph>"

        graph = self.graph_loader.load_next_graph(lines)

        self.assertEqual("TestGraph", graph.get_unique_identifier())
        self.assertEqual(0, len(graph.get_vertices()))

    def testLoadEmptyGraphWithWeirdWhitespace(self):
        lines = "<graph name=TestGraph>\t\t\n" \
                + "\n   </graph>\t"

        graph = self.graph_loader.load_next_graph(lines)

        self.assertEqual("TestGraph", graph.get_unique_identifier())
        self.assertEqual(0, len(graph.get_vertices()))

    def testLoadSingleConstant(self):
        lines = "<graph name=TestGraph>" \
                + "<component name=TestConstant>"\
                + "<class>Constant</class>"\
                + "<package>basic</package>"\
                + "</component>"\
                + "</graph>"

        graph = self.graph_loader.load_next_graph(lines)

        self.assertEqual(2, len(graph.get_vertices()))

        constant = graph.get_vertices()[0]

        self.assertEqual("TestConstant", constant.get_unique_identifier())

    def testLoadConstantWithValue(self):
        lines = "<graph name=TestGraph>" \
                + "<component name=TestConstant>"\
                + "<class>Constant</class>"\
                + "<package>basic</package>"\
                + "<attribute key=value>27</attribute>"\
                + "</component>"\
                + "</graph>"

        graph = self.graph_loader.load_next_graph(lines)
        constant = graph.get_vertices()[0]

        self.assertEqual("27", constant.get_attributes()['value'])

    def testLoadConstantWithExtraAttribute(self):
        lines = "<graph name=TestGraph>" \
                + "<component name=TestConstant>"\
                + "<class>Constant</class>"\
                + "<package>basic</package>"\
                + "<attribute key=xyz>test</attribute>"\
                + "</component>"\
                + "</graph>"

        graph = self.graph_loader.load_next_graph(lines)
        constant = graph.get_vertices()[0]

        self.assertTrue("xyz" in constant.get_attributes())
        self.assertEqual("test", constant.get_attributes()['xyz'])

    def testLoadConstantAndSigmoid(self):
        lines = "<graph name=TestGraph>" \
                + "<component name=TestConstant>"\
                + "<class>Constant</class>"\
                + "<package>basic</package>"\
                + "</component>"\
                + "<component name=TestSigmoid>"\
                + "<class>Sigmoid</class>"\
                + "<package>nonlinearities</package>"\
                + "</component>"\
                + "</graph>"

        graph = self.graph_loader.load_next_graph(lines)

        self.assertEqual(5, len(graph.get_vertices()))

        constant = graph.get_vertices()[0]
        sigmoid = graph.get_vertices()[3]

        self.assertEqual("TestConstant", constant.get_unique_identifier())
        self.assertEqual("TestSigmoid", sigmoid.get_unique_identifier())

    def testLoadConstantAndSigmoidWithLink(self):
        constant_out_name = "Output"
        sigmoid_in_name = "Input"

        lines = "<graph name=TestGraph>" \
                + "<component name=TestConstant>"\
                + "<class>Constant</class>"\
                + "<package>basic</package>"\
                + "</component>"\
                + "<component name=TestSigmoid>"\
                + "<class>Sigmoid</class>"\
                + "<package>nonlinearities</package>"\
                + "<socket name="+sigmoid_in_name+">TestConstant:"+constant_out_name+"</socket>"\
                + "</component>"\
                + "</graph>"

        graph = self.graph_loader.load_next_graph(lines)

        self.assertEqual(5, len(graph.get_vertices()))

        constant_out = graph.get_vertices()[1]
        sigmoid_in = graph.get_vertices()[2]

        self.assertEqual(1, len(constant_out.get_edges_out()))
        self.assertEqual(1, len(sigmoid_in.get_edges_in()))
        self.assertEqual(sigmoid_in, constant_out.get_edges_out()[0].destination)
        self.assertEqual(constant_out, sigmoid_in.get_edges_in()[0].origin)