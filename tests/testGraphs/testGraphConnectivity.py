import unittest
from graph.vertex import Vertex

class GraphConnectivityTest(unittest.TestCase):

    def testSingletonHasGraph(self):
        vertex = Vertex()
        self.assertIsNotNone(vertex.get_graph())

    def testSingletonGraphsDifferent(self):
        vertex1 = Vertex()
        vertex2 = Vertex()

        self.assertNotEqual(vertex1.get_graph(), vertex2.get_graph())

    def testEdgeAddedToGraph(self):
        vertex1 = Vertex()
        vertex1.add_edge(vertex1)
        self_edge = vertex1.get_edges_out()[0]

        self.assertIsNotNone(self_edge.get_graph())
        self.assertEqual(vertex1.get_graph(), self_edge.get_graph())

    def testSingletonsJoined(self):
        vertex1 = Vertex()
        vertex2 = Vertex()

        vertex1.add_edge(vertex2)

        self.assertEqual(vertex1.get_graph(), vertex2.get_graph())

    def testJoinPreservesOriginGraph(self):
        vertex1 = Vertex()
        vertex2 = Vertex()
        graph = vertex1.get_graph()

        vertex1.add_edge(vertex2)

        self.assertEqual(vertex1.get_graph(), graph)
        self.assertEqual(vertex2.get_graph(), graph)


    def testLargerGraphsJoined(self):
        vertex1 = Vertex()
        vertex2 = Vertex()

        vertex1.add_edge(vertex2)

        vertex3 = Vertex()
        vertex4 = Vertex()

        vertex3.add_edge(vertex4)

        self.assertNotEqual(vertex1.get_graph(), vertex3.get_graph())

        vertex1.add_edge(vertex3)

        self.assertEqual(vertex1.get_graph(), vertex3.get_graph())
        self.assertEqual(vertex1.get_graph(), vertex4.get_graph())
        self.assertEqual(vertex2.get_graph(), vertex3.get_graph())
        self.assertEqual(vertex2.get_graph(), vertex4.get_graph())

