import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from block_utils import markdown_to_html_node

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

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
This is text that _should_ remain
the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
> that spans multiple lines.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a blockquote that spans multiple lines.</p></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- **Bolded** item 2
- Item _3_
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li><b>Bolded</b> item 2</li><li>Item <i>3</i></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with `code`
3. Third item with _italic_
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <code>code</code></li><li>Third item with <i>italic</i></li></ol></div>",
        )

    def test_headings(self):
        md = """
# Heading 1
## Heading 2
### Heading 3 with **bold**
#### Heading 4 with _italic_
##### Heading 5 with `code`
###### Heading 6
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading 1</h1>"
            "<h2>Heading 2</h2>"
            "<h3>Heading 3 with <b>bold</b></h3>"
            "<h4>Heading 4 with <i>italic</i></h4>"
            "<h5>Heading 5 with <code>code</code></h5>"
            "<h6>Heading 6</h6>"
            "</div>",
        )

if __name__ == "__main__":
    unittest.main()
