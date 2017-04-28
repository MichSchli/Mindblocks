import unittest
from unittest.mock import MagicMock as Mock
from unittest.mock import call

from components.basic.constant import Constant
from module_management.module_importer import ModuleImporter
from persistence.graph_saver import GraphSaver
from graph.graph import Graph
from graph.vertex import Vertex


class GraphSaverTest(unittest.TestCase):

    def setUp(self):
        self.module_importer = ModuleImporter()
        self.graph_saver = GraphSaver()

    def tearDown(self):
        self.graph_saver = None


    def testYieldsHeaderAndFooter(self):
        v1 = Vertex()
        v2 = Vertex()
        v1.add_edge(v2)
        graph = v1.get_graph()
        v1.unique_identifier = "v1"
        v2.unique_identifier = "v2"
        graph.unique_identifier = "test"

        lines = list(self.graph_saver.process(graph))
        self.assertEqual(lines[0], "\t<graph name=test>")
        self.assertEqual(lines[-1], "\t</graph>")

    def testYieldsVertexHeaders(self):
        v1 = Vertex()
        v2 = Vertex()
        v1.add_edge(v2)
        graph = v1.get_graph()
        v1.unique_identifier = "v1"
        v2.unique_identifier = "v2"
        graph.unique_identifier = "test"

        lines = list(self.graph_saver.process(graph))

        self.assertEqual("\t\t<component name=v1>", lines[1])
        self.assertEqual("\t\t</component>", lines[2])
        self.assertEqual("\t\t<component name=v2>", lines[3])
        self.assertEqual("\t\t</component>", lines[5])

    def testYieldsVertexAttributes(self):
        v1 = Vertex()
        graph = v1.get_graph()
        v1.unique_identifier = "v1"
        v1.attributes['test_attribute'] = 'abc'
        graph.unique_identifier = "test"

        lines = list(self.graph_saver.process(graph))
        self.assertEqual(lines[1], "\t\t<component name=v1>")
        self.assertEqual(lines[2], "\t\t\t<attribute key=test_attribute>abc</attribute>")
        self.assertEqual(lines[3], "\t\t</component>")

    def testYieldsManifestInstructions(self):
        v1 = Vertex()
        graph = v1.get_graph()
        v1.unique_identifier = "v1"
        v1.manifest = {"name": "TestClassName", "package": "TestPackageName"}
        v1.attributes['test_attribute'] = 'abc'
        graph.unique_identifier = "test"

        lines = list(self.graph_saver.process(graph))
        self.assertEqual(lines[1], "\t\t<component name=v1>")
        self.assertEqual(lines[2], "\t\t\t<class>TestClassName</class>")
        self.assertEqual(lines[3], "\t\t\t<package>TestPackageName</package>")
        self.assertEqual(lines[4], "\t\t\t<attribute key=test_attribute>abc</attribute>")
        self.assertEqual(lines[5], "\t\t</component>")


    def testIntegrationBasicConstant(self):
        module = self.module_importer.load_package_module('basic')
        component = module.get_component("Constant")
        constant = component.instantiate()

        # Bit of a hack till we have better handling of IDs
        constant.unique_identifier = "TestConstant"

        # Change value from default to be sure
        constant.attributes['value'] = '27'

        lines = list(self.graph_saver.process(constant.get_graph()))
        self.assertEqual("\t\t<component name=TestConstant>", lines[1])
        self.assertIn("\t\t\t<class>Constant</class>", lines[2:-2])
        self.assertIn("\t\t\t<package>basic</package>", lines[2:-2])
        self.assertIn("\t\t\t<attribute key=value>27</attribute>", lines[2:-2])
        self.assertEqual("\t\t</component>", lines[-2])


    def testYieldsLinks(self):
        v1 = Vertex()
        v2 = Vertex()
        edge = v1.add_edge(v2)
        graph = v1.get_graph()
        v1.unique_identifier = "v1"
        v2.unique_identifier = "v2"
        graph.unique_identifier = "test"

        edge.attributes['in_socket'] = "TestInName"
        edge.attributes['out_socket'] = "TestOutName"

        lines = list(self.graph_saver.process(graph))
        self.assertEqual("\t\t<component name=v1>", lines[1])
        self.assertEqual("\t\t</component>", lines[2])
        self.assertEqual("\t\t<component name=v2>", lines[3])
        self.assertEqual("\t\t\t<link socket=TestInName>v1:TestOutName</link>", lines[4])
        self.assertEqual("\t\t</component>", lines[5])


    def testLargerIntegration(self):
        pass

    def testYieldsComponentLocations(self):
        pass


