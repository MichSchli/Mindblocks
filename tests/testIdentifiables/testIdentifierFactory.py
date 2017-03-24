import unittest
from identifiables.identifierFactory import IdentifierFactory
from identifiables.identifiable import Identifiable


class IdentifierFactoryTest(unittest.TestCase):

    def testGetIdentifierDefaultName(self):
        i = IdentifierFactory()
        uid = i.get_next_identifier()

        self.assertEqual(uid, "default_0")

    def testGetIdentifierChosenName(self):
        i = IdentifierFactory()
        uid = i.get_next_identifier(name_string="test_name")

        self.assertEqual(uid, "test_name_0")

    def testGetIdentifierNameIncrements(self):
        i = IdentifierFactory()
        uid1 = i.get_next_identifier(name_string="test_name")
        uid2 = i.get_next_identifier(name_string="test_name")
        uid3 = i.get_next_identifier(name_string="test_name")

        self.assertEqual(uid1, "test_name_0")
        self.assertEqual(uid2, "test_name_1")
        self.assertEqual(uid3, "test_name_2")

    def testGetIdentifierNameIncrementsOnlyIfNameSimilar(self):
        i = IdentifierFactory()
        uid1 = i.get_next_identifier(name_string="test_name")
        uid2 = i.get_next_identifier(name_string="other_test_name")
        uid3 = i.get_next_identifier(name_string="test_name")
        uid4 = i.get_next_identifier(name_string="other_test_name")

        self.assertEqual(uid1, "test_name_0")
        self.assertEqual(uid2, "other_test_name_0")
        self.assertEqual(uid3, "test_name_1")
        self.assertEqual(uid4, "other_test_name_1")

    def testGetIdentifierNameSeparatorCanBeChanged(self):
        i = IdentifierFactory()
        uid = i.get_next_identifier(name_string="test_name", separator=".")
        self.assertEqual(uid, "test_name.0")

    def testCanAssignIdentifierFromName(self):
        i = IdentifierFactory()
        o = Identifiable(name="test_name")
        i.assign_identifier(o)

        self.assertEqual(o.get_unique_identifier(), "test_name_0")


    def testAssignIdentifierIncrements(self):
        i = IdentifierFactory()
        o = Identifiable(name="test_name")
        i.assign_identifier(o)

        o = Identifiable(name="test_name")
        i.assign_identifier(o)

        self.assertEqual(o.get_unique_identifier(), "test_name_1")