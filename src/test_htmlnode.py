import unittest

from htmlnode import HTMLNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href":"boot.dev", "on_click":"func()"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="boot.dev" on_click="func()"')

    def test_default(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_td(self):
        node = LeafNode("td", "Hello, world!")
        self.assertEqual(node.to_html(), "<td>Hello, world!</td>")


    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")


if __name__ == "__main__":
    unittest.main()
