import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode
import textnode

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
            return HTMLNode(tag="img", value=text_node.text, props={"src":text_node.url})

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.NORMAL)]
    text_nodes = split_nodes_delimiter(text_nodes, TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, TextType.CODE)
    text_nodes = split_nodes_delimiter(text_nodes, TextType.CODE)
    text_nodes = split_nodes_images(text_nodes)
    text_nodes = split_nodes_links(text_nodes)
    return text_nodes


def split_nodes_delimiter(old_nodes: list[TextNode], text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            elements = node.text.split(text_type.delimiter)
            if len(elements) % 2 == 0:
                raise Exception("Invalid Markdown Syntax, every delimiter must have a matching pair")
            for i in range(len(elements)):
                if i % 2 == 0:
                    if elements[i] == "":
                        continue
                    new_nodes.append(TextNode(text=elements[i], text_type=TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(text=elements[i], text_type=text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_images(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            process(node.text, new_nodes, extract_markdown_images, TextType.IMAGE, lead='!')
    return new_nodes

def split_nodes_links(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            process(node.text, new_nodes, extract_markdown_links, TextType.LINK)
    return new_nodes

def process(text: str, new_nodes: list[TextNode], extract, text_type, lead=''):
        hyper = extract(text)
        if(hyper == []):
            if text:
                new_nodes.append(TextNode(text, TextType.NORMAL))
            return new_nodes
        alt_text, link = hyper[0][0], hyper[0][1]
        start, end = text.split(f"{lead}[{alt_text}]({link})", 1)
        if start:
            new_nodes.append(TextNode(start, TextType.NORMAL))
        new_nodes.append(TextNode(alt_text, text_type, link))
        return process(end, new_nodes, extract, text_type, lead)


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]+)\]\(([^\(\)]+)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)", text)
