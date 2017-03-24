import unittest

from graph.edge import Edge
from graph.vertex import Vertex


class GraphCreationTest(unittest.TestCase):

    def testEdgesCreatedWithOriginAndDestination(self):
        v1 = Vertex()
        v2 = Vertex()

        e = Edge(v1, v2)

        self.assertEqual(e.get_origin(), v1)
        self.assertEqual(e.get_destination(), v2)

    def testEdgesCreatedUnsatisfied(self):
        v1 = Vertex()
        v2 = Vertex()

        e = Edge(v1, v2)

        self.assertFalse(e.satisfied)

