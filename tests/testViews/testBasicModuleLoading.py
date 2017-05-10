import unittest
from unittest.mock import MagicMock as Mock

from views.view import View


class BasicModuleLoadTest(unittest.TestCase):

    def setUp(self):
        self.mock_module_1 = Mock()
        self.mock_module_2 = Mock()

        self.mm = Mock()
        self.mm.fetch_basic_modules.return_value = [self.mock_module_1, self.mock_module_2]
        self.idf = Mock()

    def tearDown(self):
        self.mm = None
        self.idf = None
        self.mock_module_1 = None
        self.mock_module_2 = None

    def testInitializedProperly(self):
        view = View("test_view", self.mm, self.idf)

        self.assertEqual(view.name, "test_view")
        self.assertEqual(view.module_manager, self.mm)
        self.assertEqual(view.identifier_factory, self.idf)
        self.assertEqual(view.available_modules, [])
        self.assertEqual(view.defined_graphs, [])

    def testLoadsModules(self):
        view = View("test_view", self.mm, self.idf)
        view.load_modules()

        self.mm.fetch_basic_modules.assert_called_with("test_view")
        self.assertEqual(len(view.get_available_modules()), 2)
        self.assertEqual(view.get_available_modules()[0], self.mock_module_1)
        self.assertEqual(view.get_available_modules()[1], self.mock_module_2)