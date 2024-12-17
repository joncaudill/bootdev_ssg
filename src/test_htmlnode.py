import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("tagtest", "valuetest", "childrentest", "propstest")
        expected = "HTMLNode(tagtest, valuetest, childrentest, propstest)"
        actual = node.__repr__()
        self.assertEqual(expected, actual)

    def test_props_to_html(self):
        testprops = {"testprop" : "yay"}
        node = HTMLNode(props=testprops)
        expected = " testprop=\"yay\""
        actual = node.props_to_html()
        self.assertEqual(expected, actual)

    def test_constructor_empty(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

if __name__ == "__main__":
    unittest.main()