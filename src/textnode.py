from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

    @property
    def delimiter(self):
        if self == TextType.BOLD:
            return "**"
        elif self == TextType.ITALIC:
            return "_"
        elif self == TextType.CODE:
            return "`"
        return None

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str|None = url 

    def __eq__(self, value) -> bool:
        return (self.text == value.text 
            and self.text_type == value.text_type 
            and self.url == value.url)

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
