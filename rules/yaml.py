#!/usr/bin/python3
from collections import OrderedDict


class YAMLNode:
    def __init__(self):
        self.level = 0
        self.key = ""
        self.value = None
        self.children = OrderedDict()
        self.parent = None

    def add_child(self, node):
        assert node.key
        self.children[node.key] = node
        node.parent = self

    def print(self):
        if self.level >= 0:
            print(self)

        for node in self.children.values():
            node.print()

    def __getitem__(self, key):
        return self.children[key]

    def __contains__(self, key):
        return key in self.children

    def __str__(self):
        if self.level < 0:
            return ""

        line = "\t" * self.level
        line += self.key + ":"
        if self.value is not None:
            line += " " + self.value
        return line


def get_indent_level(line):
    level = 0
    for ch in line:
        if ch == "\t":
            level += 1
        else:
            break
    return level


def find_match(last_node, level):
    """
    :param last_node: Last parsed node
    :param level: Level of the new child to be added to the tree
    :return: The matching node
    """
    t = last_node
    while t.level >= level:
        t = t.parent
    return t


def load_from_file(fname):
    root = YAMLNode()
    root.level = -1
    last_node = root
    prev_indent = 0

    with open(fname) as f:
        for line in f:
            if line.lstrip().startswith("#"):
                continue

            # no empty lines.
            if not line.strip():
                continue

            # We have tab indenting in OpenRA.
            assert not line.startswith(" ")

            data = [d.strip() for d in line.split(":", 1)]

            node = YAMLNode()
            node.level = get_indent_level(line)
            node.key = data[0]
            if len(data) == 2 and data[1]:
                node.value = data[1]

            par = find_match(last_node, node.level)
            par.add_child(node)

            last_node = node

    return root
