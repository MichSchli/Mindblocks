import unittest

from NEW.model.identifiables import Identifiable


class IdentifiableTest(unittest.TestCase):

    def testInitializationWithUID(self):
        i = Identifiable(unique_identifier="testIdentifier")
        self.assertEqual(i.get_unique_identifier(), "testIdentifier")

    def testInitializationWithName(self):
        i = Identifiable(name="testName")
        self.assertEqual(i.get_name(), "testName")
        self.assertIsNone(i.get_unique_identifier())

    def testAssignIdentifier(self):
        i = Identifiable(name="testName")
        i.set_unique_identifier("testIdentifier")
        self.assertEqual(i.get_unique_identifier(), "testIdentifier")

