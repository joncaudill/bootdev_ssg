import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_check_to_html_loaded_tag(self):
        the_props = {
            "href" : "https://boot.dev"
        }
        test_leaf = LeafNode("a", "Link", the_props )
        expected = "<a href=\"https://boot.dev\">Link</a>"
        actual = test_leaf.to_html()
        self.assertEqual(expected,actual)

    def test_check_to_html_no_value(self):
        the_props = {
            "style" : "font-color:red;"
        }
        test_leaf = LeafNode("p", props=the_props )
        self.assertRaises(ValueError, test_leaf.to_html)

    def test_check_to_html_no_props(self):
        test_leaf = LeafNode("p", "boogers" )
        expected = "<p>boogers</p>"
        actual = test_leaf.to_html()
        self.assertEqual(expected,actual)

    def test_check_to_html_no_tag(self):
        the_props = {
            "href" : "https://boot.dev"
        }
        test_leaf = LeafNode(value="Link", props=the_props )
        expected = "Link"
        actual = test_leaf.to_html()
        self.assertEqual(expected,actual)

if __name__ == "__main__":
    unittest.main()