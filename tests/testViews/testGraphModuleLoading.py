import unittest
from unittest.mock import MagicMock as Mock

from views.view import View


class GraphModuleLoadTest(unittest.TestCase):

    def setUp(self):
        self.mock_module_1 = Mock()
        self.mock_module_2 = Mock()
        self.mock_module_3 = Mock()

        self.mm = Mock()
        self.mm.fetch_basic_modules.return_value = [self.mock_module_1, self.mock_module_2]
        self.mm.fetch_graph_modules.return_value = [self.mock_module_3]
        self.idf = Mock()

    def tearDown(self):
        self.mm = None
        self.idf = None
        self.mock_module_1 = None
        self.mock_module_2 = None
        self.mock_module_3 = None

    def testLoadsModules(self):
        view = View("test_view", self.mm, self.idf)
        view.load_modules()

        self.mm.fetch_graph_modules.assert_called_with(view="test_view")
        self.assertEqual(len(view.get_available_modules()), 3)
        self.assertEqual(view.get_available_modules()[0], self.mock_module_1)
        self.assertEqual(view.get_available_modules()[1], self.mock_module_2)
        self.assertEqual(view.get_available_modules()[2], self.mock_module_3)