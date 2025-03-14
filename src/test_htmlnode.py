import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_many_children(self):
        child_node_1 = LeafNode("span", "child")
        child_node_2 = LeafNode("i", "i'm italian")
        child_node_3 = LeafNode("p", "deez nuts")

        parent_node = ParentNode("div", [child_node_1, child_node_2, child_node_3])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><i>i'm italian</i><p>deez nuts</p></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
