import unittest
from unittest.mock import MagicMock as Mock

from views.view import View


class ViewEdgeCreationTest(unittest.TestCase):

    def setUp(self):
        self.mm = Mock()
        self.idf = Mock()

        self.component_1 = Mock()
        module_component_1 = Mock()
        module_component_1.instantiate.return_value = self.component_1

        self.component_2 = Mock()
        module_component_2 = Mock()
        module_component_2.instantiate.return_value = self.component_2

        self.graph_1 = Mock()
        self.component_1.get_graph.return_value = self.graph_1

        self.graph_2 = Mock()
        self.component_2.get_graph.return_value = self.graph_2

        self.view = View("test_view", self.mm, self.idf)
        self.view.instantiate(module_component_1)
        self.view.instantiate(module_component_2)

    def tearDown(self):
        self.mm = None
        self.idf = None

        self.view = None
        self.component_1 = None
        self.component_2 = None

    def testGraphEdgeAdded(self):
        self.view.create_edge(self.component_1, self.component_2)
        self.component_1.add_edge.assert_called_with(self.component_2)

    def testDestinationGraphDeletedFromView(self):
        self.view.create_edge(self.component_1, self.component_2)

        self.assertEqual(len(self.view.get_defined_graphs()), 1)
        self.assertEqual(self.view.get_defined_graphs()[0], self.graph_1)

    def testDestinationGraphDeletedFromModuleManager(self):
        self.view.create_edge(self.component_1, self.component_2)

        self.mm.delete_graph.assert_called_with("test_view", self.graph_2)
