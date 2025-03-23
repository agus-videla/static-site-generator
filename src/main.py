from os.path import isfile
import shutil
from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode
import os
from shutil import rmtree

def delete_public_files():
    if os.path.exists("public"):
        rmtree("public")

def copy_to_public(source, target):
    if not os.path.exists(target):
        os.mkdir(target)
    entries = os.listdir(source)
    print(entries)
    for entry in entries:
        src = os.path.join(source, entry)
        if os.path.isdir(src):
            new_dir = os.path.join(target, entry)
            copy_to_public(src, new_dir)
        else:
            shutil.copy(src, target)
            
            

def main():
    delete_public_files()
    copy_to_public(source="static", target="public")


main()
