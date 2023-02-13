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
        nodes_stack: list[Node[U]] = []
        nodes_stack.append(self.root)

        while nodes_stack:
            current_node = nodes_stack.pop(0)
            nodes_stack = current_node.children + nodes_stack
            yield current_node
