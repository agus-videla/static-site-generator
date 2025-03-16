def markdown_to_blocks(markdown: str):
    result = []
    for block in markdown.split('\n\n'):
        stripped_lines = map(lambda x: x.strip(), block.split('\n'))
        filtered = filter(lambda x: x != '', stripped_lines)
        result.append('\n'.join(filtered))
    return result
