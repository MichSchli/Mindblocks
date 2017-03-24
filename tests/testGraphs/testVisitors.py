import unittest
from graph.vertex import Vertex
from graph.visitor import Visitor
from unittest.mock import MagicMock as Mock

class GraphVisitorTest(unittest.TestCase):

    def setUp(self):
        self.v1 = Vertex()
        self.v2 = Vertex()

        self.v1.add_edge(self.v2)
        self.graph = self.v1.get_graph()

    def tearDown(self):
        self.graph = None

    def testGenericVisitorUsesTopologicalWalk(self):
        self.graph.topological_walk = Mock()
        visitor = Visitor()
        visitor.run_visit(self.graph, lambda x: x)

        self.graph.topological_walk.assert_called_with()

    def testCallVisitorExecutesAtAllVertices(self):
        visitor = Visitor()

        fn = Mock()

        visitor.run_visit(self.graph, fn)
        self.assertEqual(fn.call_count,2)


    def testYieldVisitorYieldsAtAllSteps(self):
        visitor = Visitor()

        def fn(x, arguments=None):
            yield x

        result = list(visitor.yield_visit(self.graph, fn))

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], self.v1)
        self.assertEqual(result[1], self.v2)