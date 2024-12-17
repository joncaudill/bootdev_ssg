from textnode import TextNode, TextType
from ssg_helpers import *


def main():
    #dummy = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    #print(dummy)
    #text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    #print(extract_markdown_links(text))
    #t2tn_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    #the_textnodes = text_to_textnodes(t2tn_text)
    #markdown= '''# This is a heading

#This is a paragraph of text. It has some **bold** and *italic* words inside of it.

#* This is the first list item in a list block
#* This is a list item
#* This is another list item"'''
    #blocks = markdown_to_blocks(markdown)
    #for block in blocks:
    #    print(block_to_block_type(block))
    #html_nodes = markdown_to_html_node(markdown)
    #print(html_nodes)
    create_public()
    #generate_page("content/majesty/index.md", "template.html", "content/html")
    #markdown = '''1. Gandalf
#2. Bilbo
#3. Sam
#4. Glorfindel
#5. Galadriel
#6. Elrond
#7. Thorin
#8. Sauron
#9. Aragorn'''
#    block_to_block_type(markdown)
    generate_pages_recursive("content", "template.html", "public")

main()

