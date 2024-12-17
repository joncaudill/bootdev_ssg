import re
import os
import shutil

from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src":text_node.url,"alt":text_node.text})
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        #if node.text.count(delimiter) == 0:
        #    raise Exception("delimeter not found")
        if node.text.count(delimiter) % 2 > 0:
            raise Exception("Missing closing delimeter")
        split_old_node = node.text.split(delimiter)
        mode = False
        for split in split_old_node:
            if split == '':
                mode = not(mode)
                continue
            if mode:
                new_nodes.append(TextNode(split,text_type))
            else: 
                new_nodes.append(TextNode(split,TextType.TEXT))
            mode = not(mode)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"\!\[(.+?)\]\((.+?)\)"
    matches = re.findall(pattern,text)
    return matches

def extract_markdown_links(text):
    pattern = r"\[(.+?)\]\((.+?)\)"
    matches = re.findall(pattern,text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        mode = False
        pattern = r"(\!\[.+?\]\(.+?\))"
        split_old_node = re.split(pattern, node.text)
        #print(split_old_node)
        #skipflag = False
        for split in split_old_node:
            #if skipflag:
            #    skipflag = False
            #    continue
            if split == '':
                mode = not(mode)
                continue
            if not mode:
                new_nodes.append(TextNode(split,TextType.TEXT))
            else: 
                pattern = r"\!\[(.+?)\]\((.+?)\)"
                imgpart = re.findall(pattern,split)
                #print(f"imgpart: {imgpart}")
                new_nodes.append(TextNode(imgpart[0][0],TextType.IMAGE,imgpart[0][1]))
                #skipflag = True
            mode = not(mode)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        mode = False
        pattern = r"(\[.+?\]\(.+?\))"
        split_old_node = re.split(pattern, node.text)
        #print(split_old_node)
        #skipflag = False
        for split in split_old_node:
            #if skipflag:
            #    skipflag = False
            #    continue
            if split == '':
                mode = not(mode)
                continue
            if mode:
                pattern = r"\[(.+?)\]\((.+?)\)"
                imgpart = re.findall(pattern,split)
                #print(f"imgpart: {imgpart}")
                new_nodes.append(TextNode(imgpart[0][0],TextType.LINK,imgpart[0][1]))
            #    skipflag = True
            else: 
                new_nodes.append(TextNode(split,TextType.TEXT))
            mode = not(mode)
    return new_nodes

def text_to_textnodes(text):
    initial_textnodes = [TextNode(text, TextType.TEXT)]
    image_step = split_nodes_image(initial_textnodes)
    #print(image_step)
    link_step = split_nodes_link(image_step)
    #print(link_step)
    bold_step = split_nodes_delimiter(link_step, "**", TextType.BOLD)
    #print(bold_step)
    italic_step = split_nodes_delimiter(bold_step, "*", TextType.ITALIC)
    code_step = split_nodes_delimiter(italic_step, "`", TextType.CODE)
    #print(f"original text: {text}")
    #print(f"final output: {code_step}")
    return code_step

def markdown_to_blocks(markdown):
    initial_list = markdown.split("\n\n")
    temp_list = []
    for item in initial_list:
        temp = item.strip()
        if temp:
            temp_list.append(temp)
    new_list = list(filter(None, temp_list))
    #print(new_list)
    return new_list

def block_to_block_type(block_of_markdown):
    pattern = r"(\#{1,6}) "
    possible_block = block_of_markdown.split("\n")
    #print(block_of_markdown)
    #print(re.search(pattern, block_of_markdown))
    is_heading = False
    if re.search(pattern,block_of_markdown):
        is_heading = True
    #is_heading = (re.search(pattern,block_of_markdown) == 0)
    is_codeblock = ((block_of_markdown[0:4] == '```') and (block_of_markdown[-3:] == '```'))
    is_quote_block = True
    is_ul_block = True
    is_ordered_list_block = False
    pattern = r"(\d+?\.)"
    for line in possible_block:
        if not (line[0] == ">"):
            is_quote_block = False
        #print(f"test: '{line[:2]}'")
        if not ((line[:2] == "* ") or (line[:2] == "- ")):
            is_ul_block = False
        partline = line.split(" ")[0]
        #print(f"partline:'{partline}'")
        #print(f"regex:'{(re.findall(pattern,partline))[0]}'")
        regex_ol_check = re.findall(pattern,partline)
        if len(regex_ol_check) > 0:
            if (partline == (re.findall(pattern,partline))[0]):
                is_ordered_list_block = True
    if is_heading: 
        return "heading"
    if is_codeblock: 
        return "code"
    if is_quote_block:
        return "quote"
    if is_ul_block:
        return "unordered_list"
    if is_ordered_list_block:
        return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown):
    list_of_html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        lines_in_block = block.split("\n")
        #print(f"{type(block)} block coming in: {block}")
        block_type = block_to_block_type(block)
        match(block_type):
            case "heading":
                parsed = block.split(" ", maxsplit=1)
                level = len(parsed[0])
                list_of_html_nodes.append(LeafNode(f"h{level}", parsed[1]))
            case "code":
                list_of_html_nodes.append(LeafNode("code", block.strip("`")))
            case "quote":
                new_block = []
                for lines in block:
                    new_block.append(lines.lstrip(">"))
                list_of_html_nodes.append(LeafNode("blockquote", ("".join(new_block)).strip()))
            case "unordered_list":
                child_items = []
                for line in lines_in_block:
                    li_value = line[2:]
                    #print(f"~~~line: {line}~~~~")
                    text_nodes = text_to_textnodes(li_value)
                    html_nodes = []
                    for node in text_nodes:
                        html_nodes.append(text_node_to_html_node(node))
                    child_items.append(ParentNode("li", html_nodes))
                parent_item = ParentNode("ul", child_items)
                list_of_html_nodes.append(parent_item)
            case "ordered_list":
                child_items = []
                for line in lines_in_block:
                    text_part = line.split(". ", maxsplit=1)[1]
                    text_nodes = text_to_textnodes(text_part)
                    html_nodes = []
                    for node in text_nodes:
                        html_nodes.append(text_node_to_html_node(node))
                    child_items.append(ParentNode("li", html_nodes))
                parent_item = ParentNode("ol", child_items)
                list_of_html_nodes.append(parent_item)
            case "paragraph":
                text_nodes = text_to_textnodes(block)
                html_nodes = []
                for node in text_nodes:
                    html_nodes.append(text_node_to_html_node(node))
                list_of_html_nodes.append(ParentNode("p", html_nodes))
    return ParentNode("div", list_of_html_nodes)

def create_public():
    current_folder_contents = os.listdir(".")
    print(current_folder_contents)
    if os.path.exists("public/"):
        print("removing public/")    
        shutil.rmtree("public/")
        print("making public/")
        os.mkdir("public/")
    if os.path.exists("static/"):
        print("copying items from static to public")
        copy_items("static", "public")
    else:
        raise Exception("static folder doesn't exist!")
    
def copy_items(source, dest):
    if os.path.exists(source):
        path_contents = os.listdir(source)
    else:
        raise Exception("source does not exist")
    if not(os.path.exists(dest)):
        print(f"path: {dest} does not exist.  Creating...")
        os.mkdir(dest)
    for item in path_contents:
        if os.path.isfile(f"{source}/{item}"):
            print(f"copying: {source}/{item} to {dest}")
            shutil.copy(f"{source}/{item}", f"{dest}")
        else: 
            copy_items(f"{source}/{item}", f"{dest}/{item}")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[:2] == "# ":
            return (line[2:]).strip()
    raise Exception("no header in markdown file")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        md_content = md_file.read()
    with open(template_path) as template_file:
        template_content = template_file.read()
    html_nodes = markdown_to_html_node(md_content)
    print(f"html nodes: {html_nodes}")
    generated_html = html_nodes.to_html()
    page_title = extract_title(md_content)
    template_content = template_content.replace("{{ Title }}", page_title)
    template_content = template_content.replace("{{ Content }}", generated_html)
    if not(os.path.exists(template_path)):
        os.mkdir(dest_path)
    with open(f"{dest_path}/index.html", "w") as finished_file:
        finished_file.write(template_content)
    shutil.copy("content/html/index.html", "public")
    
def path_exists(path):
    return os.path.exists(path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not(path_exists(dir_path_content) and \
        path_exists(template_path)):
        raise Exception("one of the paths does not exist")
    with open(template_path) as template_data:
        template_source = template_data.read()
    filelist = os.listdir(dir_path_content)
    for file in filelist:
        if os.path.isfile(f"{dir_path_content}/{file}"):
            if file[-3:] == ".md":
                with open(f"{dir_path_content}/{file}") as md_file:
                    md_content = md_file.read()
                template_content = template_source
                html_nodes = markdown_to_html_node(md_content)
                generated_html = html_nodes.to_html()
                page_title = extract_title(md_content)
                template_content = template_content.replace("{{ Title }}", page_title)
                template_content = template_content.replace("{{ Content }}", generated_html)
                if not(os.path.exists(dest_dir_path)):
                    os.mkdir(dest_dir_path)
                out_file = file[:-3] + ".html"
                with open(f"{dest_dir_path}/{out_file}", "w") as finished_file:
                    finished_file.write(template_content)
        else:
            if not(os.path.exists(f"{dest_dir_path}/{file}")):
                os.mkdir(f"{dest_dir_path}/{file}")
            generate_pages_recursive(f"{dir_path_content}/{file}", template_path, f"{dest_dir_path}/{file}")
            


