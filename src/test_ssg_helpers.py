import unittest

from textnode import TextType, TextNode
from leafnode import LeafNode
from ssg_helpers import (text_node_to_html_node,  
        split_nodes_delimiter, 
        extract_markdown_images, 
        extract_markdown_links,  
        split_nodes_image,  
        split_nodes_link, 
        text_to_textnodes, 
        markdown_to_blocks,
        block_to_block_type,
        extract_title)

class TestMain(unittest.TestCase):
    def test_textnode_to_html_node_text(self):
        the_textnode = TextNode("test", TextType.TEXT)
        expected = LeafNode(None, "test")
        actual = text_node_to_html_node(the_textnode)
        self.assertEqual(actual, expected)

    def test_split_nodes_delimiter(self):
        testnode = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([testnode], "`", TextType.CODE)
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT)]       
        self.assertEqual(actual,expected)

    def test_extract_markdown_images(self):
        testtext = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_images(testtext)
        expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(actual,expected)

    def test_extract_markdown_images(self):
        testtext = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(testtext)
        expected = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(actual,expected)

    def test_split_nodes_link(self):
        testnode = TextNode("Test text [link](https://www.boot.dev) test", TextType.TEXT)
        actual = split_nodes_link([testnode])
        expected = [TextNode("Test text ", TextType.TEXT), TextNode("link", TextType.LINK, "https://www.boot.dev"), TextNode(" test", TextType.TEXT)]
        self.assertEqual(actual, expected)

    def test_split_nodes_image(self):
        testnode = TextNode("Test text ![alt](https://imgur.com/6969) test", TextType.TEXT)
        actual = split_nodes_image([testnode])
        expected = [TextNode("Test text ", TextType.TEXT), TextNode("alt", TextType.IMAGE, "https://imgur.com/6969"), TextNode(" test", TextType.TEXT)]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes(self):
        t2tn_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_textnodes(t2tn_text)
        expected = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev")
]
        self.assertEqual(actual,expected)

    def test_markdown_to_blocks(self):
        markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"'''
        actual = markdown_to_blocks(markdown)
        expected = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item"']
        self.assertEqual(actual, expected)

    def test_block_to_block_type(self):
        block1 = '# This is a heading'
        block2 = 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.'
        block3 = '* This is the first list item in a list block\n* This is a list item\n* This is another list item"'
        actual1 = block_to_block_type(block1)
        expected1 = "heading"
        actual2 = block_to_block_type(block2)
        expected2 = "paragraph"
        actual3 = block_to_block_type(block3)
        expected3 = "unordered_list"
        self.assertEqual(actual1,expected1)
        self.assertEqual(actual2,expected2)
        self.assertEqual(actual3,expected3)

    def test_extract_title_markdown(self):
        markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"'''
        actual = extract_title(markdown)
        expected = "This is a heading"
        self.assertEqual(actual, expected)
        