import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from textnode_utils import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_with_url(self):
        node = TextNode("This is a text node", TextType.IMAGE, "someurl.com")
        node2 = TextNode("This is a text node", TextType.IMAGE, "someurl.com")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node: HTMLNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()
