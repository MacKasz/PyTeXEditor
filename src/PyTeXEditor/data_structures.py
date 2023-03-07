from typing import Generator, TypeVar, Generic


T = TypeVar("T")


class Node(Generic[T]):
    __slots__ = ("id", "data", "children")

    def __init__(self, id: object, data: T) -> None:
        self.id = id
        self.data = data
        self.children: list[Node[T]] = []

    def add_child(self, child: "Node[T]") -> None:
        self.children.append(child)

    def __str__(self) -> str:
        output = f"({self.id}, {self.data}"
        if self.children:
            output += ", ("
            for child in self.children:
                output += f"{child.id}, "
            output = output[:-2] + ")"
        output += ")"
        return output

    def __repr__(self) -> str:
        return self.__str__()


U = TypeVar("U")


class Tree(Generic[U]):
    def __init__(self, root: Node[U]):
        self.root = root

    def preorder_traverse(self) -> Generator[Node[U], None, None]:
        """Generator to traverse the nodes in the tree, in preorder.

        Yields
        ------
        Generator[Node[U], None, None]
            Node of the Tree generic.
        """
        nodes_stack: list[Node[U]] = []
        nodes_stack.append(self.root)

        while nodes_stack:
            current_node = nodes_stack.pop(0)
            nodes_stack = current_node.children + nodes_stack
            yield current_node


if __name__ == "__main__":
    a = Node[int](1, 1)
    b = Node[int](2, 2)
    c = Node[int](3, 3)
    d = Node[int](4, 4)
    e = Node[int](5, 5)
    f = Node[int](6, 6)
    tree = Tree[int](a)
    a.add_child(b)
    a.add_child(c)
    b.add_child(d)
    b.add_child(e)
    e.add_child(f)
    for node in tree.preorder_traverse():
        print(node.id)
