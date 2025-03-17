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
    if(re.match(r"^#{1,7}\s", markdown)):
        return BlockType.HEADING
    if(re.match(r"^```[\s\S]+```$", markdown)):
        return BlockType.CODE
    if(re.match(r"", markdown)):
        return BlockType.QUOTE
    if(re.match(r"^```.+```$", markdown)):
        return BlockType.ORDERED_LIST
    if(re.match(r"^>$", markdown)):
        return BlockType.CODE
