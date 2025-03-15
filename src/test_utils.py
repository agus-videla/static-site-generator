import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from utils import split_nodes_images, split_nodes_links, text_node_to_html_node, split_nodes_delimiter, extract_markdown_links, extract_markdown_images

class TestUtils(unittest.TestCase):
    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "boot.dev")
        html_node: HTMLNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "This is an image node")
        self.assertEqual(html_node.props, {"src":"boot.dev"})

    def test_split_italics_then_bold(self):
        node = TextNode("this is _italics_ and this is **bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, TextType.BOLD)
        self.assertEqual(
                [
                    TextNode("this is ", TextType.NORMAL),
                    TextNode("italics", TextType.ITALIC),
                    TextNode(" and this is ", TextType.NORMAL),
                    TextNode("bold", TextType.BOLD),
                ],
                new_nodes
        )

    def test_split_only_code(self):
        node = TextNode("`code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], TextType.CODE)
        self.assertEqual(
                [
                    TextNode("code", TextType.CODE),
                ],
                new_nodes
        )

    def test_split_wrong_syntext(self):
        node = TextNode("this is an underscore: _", TextType.NORMAL)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], TextType.ITALIC)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("This is just normal text.", TextType.NORMAL)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([node], new_nodes)

    def test_link_at_start(self):
        node = TextNode("[Boot.dev](https://www.boot.dev) is a great site.", TextType.NORMAL)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is a great site.", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode("Check out [Boot.dev](https://www.boot.dev)", TextType.NORMAL)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.NORMAL),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_consecutive_links(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev)[YouTube](https://www.youtube.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("YouTube", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )


    def test_malformed_link(self):
        node = TextNode("Check out [Boot.dev(https://www.boot.dev)", TextType.NORMAL)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([node], new_nodes)

    def test_mixed_links_and_images(self):
        node = TextNode(
            "This is a ![logo](https://i.imgur.com/logo.png) and a [link](https://example.com).",
            TextType.NORMAL,
        )
        new_nodes_links = split_nodes_links([node])
        new_nodes_images = split_nodes_images(new_nodes_links)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.NORMAL),
                TextNode("logo", TextType.IMAGE, "https://i.imgur.com/logo.png"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(".", TextType.NORMAL),
            ],
            new_nodes_images,
        )

