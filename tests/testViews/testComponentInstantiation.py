import unittest
from unittest.mock import MagicMock as Mock

from views.view import View


class ViewComponentInstantiateTest(unittest.TestCase):

    def setUp(self):
        self.mm = Mock()
        self.idf = Mock()

    def tearDown(self):
        self.mm = None
        self.idf = None

    def testInstantiatesComponentFromModule(self):
        component = Mock()
        module_component = Mock()
        module_component.instantiate.return_value = component

        view = View("test_view", self.mm, self.idf)

        instantiated = view.instantiate(module_component)

        module_component.instantiate.assert_called_with()
        self.assertEqual(instantiated, component)

    def testInstantiateAddsGraph(self):
        component = Mock()
        module_component = Mock()
        module_component.instantiate.return_value = component

        graph = Mock()
        component.get_graph.return_value = graph

        view = View("test_view", self.mm, self.idf)
        view.instantiate(module_component)

        self.assertEqual(len(view.get_defined_graphs()), 1)
        self.assertEqual(view.get_defined_graphs()[0], graph)

    def testInstantiateAssignsUidToComponent(self):
        component = Mock()
        module_component = Mock()
        module_component.instantiate.return_value = component

        view = View("test_view", self.mm, self.idf)
        view.instantiate(module_component)

        self.idf.assign_identifier.assert_any_call(component)

    def testInstantiateAssignUidToGraph(self):

        component = Mock()
        module_component = Mock()
        module_component.instantiate.return_value = component

        graph = Mock()
        component.get_graph.return_value = graph

        view = View("test_view", self.mm, self.idf)
        view.instantiate(module_component)

        self.idf.assign_identifier.assert_any_call(graph)

    def testInstantiateRegistersGraphWithModuleManager(self):
        component = Mock()
        module_component = Mock()
        module_component.instantiate.return_value = component

        graph = Mock()
        component.get_graph.return_value = graph

        view = View("test_view", self.mm, self.idf)
        view.instantiate(module_component)

        self.mm.register_graph.assert_called_with("test_view", graph)




