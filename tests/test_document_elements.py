import pytest
from PyTeXEditor.DataStructures import Node, Tree


def test_node():
    node = Node[str](1, "node")
    child_node = Node[str](2, "child_node")
    node.children.append(child_node)

    assert node.id == 1
    assert node.data == "node"
    assert node.children == [child_node]
    assert str(node) == "(1, node, (2))"


def test_tree():
    root_node = Node[int](1, 1)
    tree = Tree(root_node)

    assert tree.root == root_node


def test_tree_traverse():
    node1 = Node[int](1, 1)
    node2 = Node[int](2, 1)
    node3 = Node[int](3, 1)
    node4 = Node[int](4, 1)
    node5 = Node[int](5, 1)
    node6 = Node[int](6, 1)

    tree = Tree(node1)
    node1.add_child(node2)
    node2.add_child(node3)
    node2.add_child(node4)

    node1.add_child(node5)
    node5.add_child(node6)

    assert tree.root == node1

    for i, current_node in zip([1, 2, 3, 4, 5, 6], tree.preorder_traverse()):
        assert i == current_node.id
