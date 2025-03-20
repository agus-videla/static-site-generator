import re
from markdown_blocks import BlockType

def markdown_to_blocks(markdown: str):
    result = []
    for block in markdown.split('\n\n'):
        stripped_lines = map(lambda x: x.strip(), block.split('\n'))
        filtered = filter(lambda x: x != '', stripped_lines)
        result.append('\n'.join(filtered))
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
