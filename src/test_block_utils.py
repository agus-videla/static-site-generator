import unittest

from block_utils import markdown_to_blocks, block_to_block_type
from markdown_blocks import BlockType

class TestUtils(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_header(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Deep Heading"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("Not a heading"), BlockType.HEADING)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nprint('Hello')\n```"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("```\nnot closed"), BlockType.CODE)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type("> Quote\nNot a quote"), BlockType.QUOTE)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item one\n2. Item two"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("3. Another item\n10. More items"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1. Item one\n- Not ordered"), BlockType.ORDERED_LIST)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item one\n- Item two"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- First item\n- Second item"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("- Item one\n1. Ordered"), BlockType.UNORDERED_LIST)
