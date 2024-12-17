import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_parentnode_tohtml_no_tag(self):
        testclass = ParentNode(None, [LeafNode(None, "poop", None)], None)
        self.assertRaises(ValueError, testclass.to_html)

    def test_parentnode_tohtml_no_children(self):
        testclass = ParentNode("p", None, None)
        self.assertRaises(ValueError, testclass.to_html)

    def test_parentnode_tohtml_child_props(self):
        testprops = {
            "style": "font-color:red;"
        }
        child = LeafNode("b", "Bold text")
        testclass = ParentNode("p", [child], testprops)
        actual = testclass.to_html()
        expected = "<p style=\"font-color:red;\"><b>Bold text</b></p>"
        self.assertEqual(actual,expected)

    def test_parentnode_tohtml_multi_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        testclass = ParentNode("p", children, None)
        actual = testclass.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(actual, expected)

    def test_parentnode_tohtml_children_grandchildren(self):
        child = LeafNode("b", "Bold text")
        parent = ParentNode("p", [child], props=None)
        grandparent = ParentNode("p", [child, parent], props=None)
        testclass = grandparent
        actual = testclass.to_html()
        expected = "<p><b>Bold text</b><p><b>Bold text</b></p></p>"
        self.assertEqual(actual, expected)
    