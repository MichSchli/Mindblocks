import unittest
from unittest.mock import MagicMock as Mock
from unittest.mock import call

from persistence.view_saver import ViewSaver
from views.view import View


class ViewSaverTest(unittest.TestCase):

    def setUp(self):
        self.view = View("test", Mock(), Mock())
        self.graph_saver = Mock()
        self.view_saver = ViewSaver(self.graph_saver)

    def tearDown(self):
        self.view = None
        self.graph_saver = None
        self.view_saver = None

    def testYieldsHeader(self):
        lines = list(self.view_saver.process(self.view))
        self.assertEqual(lines[0], "<view name="+self.view.name+">")

    def testYieldsFooter(self):
        lines = list(self.view_saver.process(self.view))
        self.assertEqual(lines[-1], "</view>")

    def testYieldsGraphs(self):
        g1 = Mock()
        g2 = Mock()

        self.view.append_graph(g1)
        self.view.append_graph(g2)

        lines = list(self.view_saver.process(self.view))

        call_args = self.graph_saver.process.call_args_list
        self.assertEqual(call_args, [call(g1), call(g2)])


