import unittest

from graph.vertex import Vertex
from module_management.module_importer import ModuleImporter
from packages.graph.subgraph_component import SubgraphComponent
from persistence.graph_saver import GraphSaver


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
        self.assertEqual("\t\t</component>", lines[4])

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

    def testSubgraphComponentYieldsSubgraph(self):
        attributes = {'target_view': 'TestView', 'target_graph': 'TestGraph'}
        sgc = SubgraphComponent()
        sgc.update_attributes(attributes)
        sgc.unique_identifier = "TestSGC"

        lines = list(self.graph_saver.process(sgc.get_graph()))
        self.assertEqual("\t\t<component name=TestSGC>", lines[1])
        self.assertIn("\t\t\t<class>SubgraphComponent</class>", lines[2:-2])
        self.assertIn("\t\t\t<package>graph</package>", lines[2:-2])
        self.assertIn("\t\t\t<attribute key=target_view>TestView</attribute>", lines[2:-2])
        self.assertIn("\t\t\t<attribute key=target_graph>TestGraph</attribute>", lines[2:-2])
        self.assertEqual("\t\t</component>", lines[-2])


    def testIntegrationConstantToSigmoid(self):
        module = self.module_importer.load_package_module('basic')
        component = module.get_component("Constant")
        constant = component.instantiate()
        constant.create_sockets()

        module2 = self.module_importer.load_package_module('nonlinearities')
        component2 = module2.get_component("Sigmoid")
        sigmoid = component2.instantiate()
        sigmoid.create_sockets()

        # Bit of a hack till we have better handling of IDs
        constant.unique_identifier = "TestConstant"
        sigmoid.unique_identifier = "TestSigmoid"

        constant.get_out_socket_by_id(0).add_edge(sigmoid.get_in_socket_by_id(0))
        constant_out_name = constant.get_out_socket_by_id(0).description['name']
        sigmoid_in_name = sigmoid.get_in_socket_by_id(0).description['name']

        # Change value from default to be sure
        constant.attributes['value'] = '27'

        lines = list(self.graph_saver.process(constant.get_graph()))

        self.assertEqual("\t\t<component name=TestConstant>", lines[1])
        self.assertEqual("\t\t\t<class>Constant</class>", lines[2])
        self.assertEqual("\t\t\t<package>basic</package>", lines[3])
        self.assertEqual("\t\t\t<attribute key=value>27</attribute>", lines[4])
        self.assertEqual("\t\t</component>", lines[5])
        self.assertEqual("\t\t<component name=TestSigmoid>", lines[6])
        self.assertEqual("\t\t\t<class>Sigmoid</class>", lines[7])
        self.assertEqual("\t\t\t<package>nonlinearities</package>", lines[8])
        self.assertEqual("\t\t\t<socket name="+sigmoid_in_name+">TestConstant:"+constant_out_name+"</socket>", lines[9])
        self.assertEqual("\t\t</component>", lines[10])

    '''
    More tests relating specifically to component/socket implementation after refactoring
    '''



