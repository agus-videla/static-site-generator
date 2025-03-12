from textnode import TextNode
from textnode import InlineText

def main():
    print(TextNode("dummy text", InlineText.IMAGE, "http://imgur.com/image"))

main()
