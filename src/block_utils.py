import re
from markdown_blocks import BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode_utils import text_to_textnodes, text_node_to_html_node

def markdown_to_blocks(markdown: str):
    result = []
    for block in markdown.split('\n\n'):
        stripped_lines = map(lambda x: x.strip(), block.split('\n'))
        filtered = filter(lambda x: x != '', stripped_lines)
        joint_block = '\n'.join(filtered)
        if joint_block:
            result.append(joint_block)
    return result

def block_to_block_type(markdown: str):
    if isHeader(markdown):
        return BlockType.HEADING
    lines = markdown.split("\n")
    if isCode(lines):
        return BlockType.CODE
    if isQuote(lines):
        return BlockType.QUOTE
    if isOrderedList(lines):
        return BlockType.ORDERED_LIST
    if isUnorderedList(lines):
        return BlockType.UNORDERED_LIST
    return BlockType.PARAGRAPH

def isQuote(lines: list[str]):
    for line in lines:
        if line[0] != ">":
            return False
    return True

def isCode(lines: list[str]):
    return lines[0] == lines[-1] == "```"

def isHeader(markdown: str):
    return re.match(r"^#{1,7}\s", markdown)

def isUnorderedList(lines: list[str]):
    for line in lines:
        if line[0] != "-":
            return False
    return True

def isOrderedList(lines: list[str]):
    for line in lines:
        if not re.match(r"\d+\.",line):
            return False
    return True

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown) 
    result = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                result.append(ParentNode(tag="p", children=text_to_children(block)))
            case BlockType.HEADING:
                for line in block.split('\n'):
                    heading = count_hashtags(line)
                    print(heading)
                    tag = f"h{heading}"
                    result.append(ParentNode(tag, text_to_children(line.lstrip(("# ")))))
            case BlockType.CODE:
                block = block.strip("```").lstrip("\n")
                result.append(ParentNode("pre", [LeafNode(tag="code", value=block)]))
            case BlockType.QUOTE:
                block = " ".join(list(map(lambda x: x.lstrip("> "), block.split('\n'))))
                result.append(ParentNode("blockquote", [LeafNode("p", value=block)]))
            case BlockType.UNORDERED_LIST:
                items = []
                for line in block.split('\n'):
                    items.append(ParentNode("li", text_to_children(line.lstrip("- "))))
                result.append(ParentNode("ul", items))
            case BlockType.ORDERED_LIST:
                items = []
                for line in block.split('\n'):
                    items.append(ParentNode("li", text_to_children(re.sub(r"^\d+\.\s+", '', line))))
                result.append(ParentNode("ol", items))
    return ParentNode(tag="div", children=result)


def text_to_children(text) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def count_hashtags(text):
    acc = 0
    for c in text.lstrip():
        if c == "#":
            acc += 1
        else:
            break
    return acc
