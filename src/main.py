from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match (text_node.text_type):
        case TextType.NORMAL:
            return HTMLNode(value=text_node.text)
        case TextType.BOLD:
            return HTMLNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return HTMLNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return HTMLNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return HTMLNode(tag="a", value=text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            return HTMLNode(tag="img", value=text_node.text, props={"src":text_node.url,"alt":text_node.alt})
        case _:
            raise ValueError("Invalid Text Type")

def main():
    print(TextNode("dummy text", TextType.IMAGE, "http://imgur.com/image"))

main()
