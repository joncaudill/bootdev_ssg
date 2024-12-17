import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_title_not_eq(self):
        node = TextNode("node 1", TextType.BOLD)
        node2 = TextNode("node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_testtype_not_eq(self):
        node = TextNode("node 1", TextType.TEXT)
        node2 = TextNode("node 1", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("node 1", TextType.BOLD, "https://microsoft.com")
        node2 = TextNode("node 1", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()