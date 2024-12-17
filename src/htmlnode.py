
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented yet.")
    
    def props_to_html(self):
        builder = ""
        if not self.props:
            return ""
        for prop in self.props:
            builder += f" {prop}=\"{self.props[prop]}\""
        return builder
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        return (self.tag == other.tag) and (self.value == other.value) and (self.children == other.children) and (self.props == other.props)
        