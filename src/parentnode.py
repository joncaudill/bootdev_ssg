from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag value.")
        
        if not self.children:
            raise ValueError("ParentNode must have a children value")
        builder = f"<{self.tag}" + super().props_to_html()
        children_string = ""
        
        for child_node in self.children:
            if child_node:
                children_string += child_node.to_html()

        builder += f">{children_string}</{self.tag}>"

        return builder
        