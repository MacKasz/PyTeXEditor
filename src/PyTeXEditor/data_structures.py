from typing import Generator, TypeVar, Generic


T = TypeVar("T")


class Node(Generic[T]):
    """Node generic class

    Attributes
    ----------
    id: int
        The id of the node.
    data: [T]
        The data of the node.
    children: list[Node]
        The children of this node.

    Methods
    -------
    add_child(child)
        Add a child node.
    """
    __slots__ = ("id", "data", "children")

    def __init__(self, id: object, data: T) -> None:
        self.id = id
        self.data = data
        self.children: list[Node[T]] = []

    def add_child(self, child: "Node[T]") -> None:
        """Adds a child node.

        Parameters
        ----------
        child : Node[T]
            The child to add.
        """
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
    """Tree data strcture

    Attributes
    ----------
    root: Node
        The root node.

    Methods
    -------
    preorder_traverse()
        Generator that traverses the tree in preorder order.
    """
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
