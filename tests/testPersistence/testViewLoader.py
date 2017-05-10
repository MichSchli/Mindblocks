import unittest
from unittest.mock import MagicMock as Mock
from module_management.module_importer import ModuleImporter
from persistence.graph_loader import GraphLoader
from persistence.view_loader import ViewLoader


class ViewSaverTest(unittest.TestCase):

    def setUp(self):
        self.module_manager = Mock()
        self.identifier_factory = Mock()
        self.graph_loader = Mock()
        self.view_loader = ViewLoader(self.graph_loader, self.module_manager, self.identifier_factory)

    def tearDown(self):
        self.graph_loader = None
        self.view_loader = None
        self.module_manager = None
        self.identifier_factory = None

    def testLoadEmptyView(self):
        lines = "<view name=TestView>" \
                + "</view>"

        view, _ = self.view_loader.load_next_view(lines)

        self.assertEqual("TestView", view.get_name())
        self.assertEqual(0, len(view.get_defined_graphs()))

    def testLoadViewsInSequence(self):
        lines = "<view name=TestView1>" \
                + "</view>" \
                + "<view name=TestView2>" \
                + "</view>"

        view1, idx = self.view_loader.load_next_view(lines)
        view2, _ = self.view_loader.load_next_view(lines, start_index=idx)

        self.assertEqual("TestView1", view1.get_name())
        self.assertEqual("TestView2", view2.get_name())

    def testLoadMultipleEmptyViews(self):
        lines = "<view name=TestView1>" \
                + "</view>" \
                + "<view name=TestView2>" \
                + "</view>" \
                + "<view name=TestView3>" \
                + "</view>"

        views = self.view_loader.load_views(lines)

        self.assertEqual("TestView1", views[0].get_name())
        self.assertEqual("TestView2", views[1].get_name())
        self.assertEqual("TestView3", views[2].get_name())

    def testLoadViewWithGraph(self):
        lines = "<view name=TestView>" \
                + "<graph name=TestGraph>" \
                + "</graph>" \
                + "</view>"

        graph = Mock()
        self.graph_loader.load_next_graph.return_value = (graph, len(lines)-7)

        view, _ = self.view_loader.load_next_view(lines)

        self.assertEqual("TestView", view.get_name())
        self.assertEqual(1, len(view.get_defined_graphs()))
        self.assertEqual(graph, view.get_defined_graphs()[0])

    def testLoadMultipleViewsWithGraphs(self):
        lines = "<view name=TestView1>" \
                + "<graph name=TestGraph1>" \
                + "</graph>" \
                + "</view>" \
                + "<view name=TestView2>" \
                + "</view>" \
                + "<view name=TestView3>" \
                + "<graph name=TestGraph2>" \
                + "</graph>" \
                + "</view>"

        graph1 = Mock()
        graph2 = Mock()
        self.graph_loader.load_next_graph.side_effect = [(graph1, 52), (graph2, len(lines)-7)]
        views = self.view_loader.load_views(lines)

        self.assertEqual(1, len(views[0].get_defined_graphs()))
        self.assertEqual(graph1, views[0].get_defined_graphs()[0])

        self.assertEqual(0, len(views[1].get_defined_graphs()))

        self.assertEqual(1, len(views[2].get_defined_graphs()))
        self.assertEqual(graph2, views[2].get_defined_graphs()[0])