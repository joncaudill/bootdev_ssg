from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        self.tag = tag
        self.value = value
        self.props = props
        super().__init__(tag, value, props=props)

    def to_html(self):
        builder = ""
        if self.tag:
            builder += "<" + self.tag
            builder += super().props_to_html()
            if self.value:
                builder += f">{self.value}</{self.tag}>"
            else:
                #raise ValueError("LeafNode.to_html() must contain a value")
                builder += f">&nbsp</{self.tag}"
            return builder
        else:
            return f"{self.value}"
