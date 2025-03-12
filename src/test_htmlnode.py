import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
