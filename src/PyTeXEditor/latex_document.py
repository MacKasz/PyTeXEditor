from PyQt6.QtGui import QTextDocument, QTextCursor, QTextFrameFormat
from PyTeXEditor.extract_latex import seperate
from PyTeXEditor.data_structures import Tree, Node
from PyTeXEditor.document_elements import (
    Block,
    get_env_regex,
    TerminalMacro,
    Environment,
    IncludeTerminator,
    ENVIRONMENTS,
    MACROS,
)
import logging


class LatexDocument(QTextDocument):
    log = logging.getLogger("LatexDocument")

    def __init__(self):
        self.plain_text: list[str] = list()
        self.intermediate: list[str] = list()
        self.object_tree: Tree[Block]
        super().__init__()

    def internal_to_qt(self) -> None:
        pass

    def __process_plaintext(self) -> None:
        self.intermediate = seperate(self.plain_text)

    def __process_intermediate(self) -> None:

        if not self.intermediate:
            self.log.error("intermediate is empty")
            return None

        document_class = ENVIRONMENTS["document"]  # type: ignore
        doc_begin, _ = get_env_regex("document")

        i = 0
        id_counter = 0
        # Scans the intermediate to get to the begin{document} macro
        while len(self.intermediate) > i:
            if doc_begin.match(self.intermediate[i]):
                # Starts the tree if the document is found
                root_object = Node[document_class](  # type: ignore
                    id_counter, document_class()
                )
                self.object_tree = Tree[Block](root_object)
                root_object.data.process_data(  # type: ignore
                    self.intermediate[i]
                )
                id_counter += 1
                break

            i += 1

        # No document, terminate early
        if not self.object_tree:
            return None

        # Cut to the document
        self.log.debug(f"Cutting at {i} (length={len(self.intermediate)})")
        self.intermediate = self.intermediate[(i + 1):]
        self.log.debug(f"After cutting: length={len(self.intermediate)}")

        # Start the stack
        node_stack: list[Node[Block]] = [self.object_tree.root]

        i = 0
        current_data = self.intermediate[i]
        while len(self.intermediate) > i:

            self.log.debug("---")
            self.log.debug(f"Current element: '{self.intermediate[i]}'")

            # Collapse terminator
            if not node_stack:
                self.log.debug("node_stack emtpy, finish")
                break
            last_node = node_stack[-1]
            last_terminator = last_node.data.terminator

            # If there is a terminator for the last node on the stack
            if last_terminator:
                if last_terminator.match(self.intermediate[i]):

                    self.log.debug(f"Found terminator {last_terminator}")
                    # Should the current item be included in the data?

                    last_include = last_node.data.include_type

                    if last_include == IncludeTerminator.BEFORE:
                        self.log.debug(f"setting data {current_data}")
                        last_node.data.process_data(current_data)
                        if node_stack:
                            node_stack.pop()
                        continue

                    elif last_include == IncludeTerminator.INCLUDE:
                        self.log.debug("Include")
                        current_data += self.intermediate[i]
                        self.log.debug(f"setting data '{current_data}'")
                        last_node.data.process_data(current_data)
                        if node_stack:
                            node_stack.pop()
                        continue

            current_data = self.intermediate[i]

            for macro_type, regex in MACROS.items():
                if regex.match(self.intermediate[i]):
                    self.log.debug(f"Element is {macro_type}")
                    new_node = Node[macro_type](  # type: ignore
                        id_counter, macro_type()
                    )
                    node_stack[-1].add_child(new_node)
                    node_stack.append(new_node)
                    # Don't add to stack

            for env_name, env_type in ENVIRONMENTS.items():
                regex, _ = get_env_regex(env_name)
                if regex.match(self.intermediate[i]):
                    self.log.debug(f"Element is {env_name}")
                    new_node = Node[env_type](  # type: ignore
                        id_counter,
                        env_type()
                    )
                    node_stack[-1].add_child(new_node)
                    node_stack.append(new_node)

            i += 1

        if node_stack:
            self.log.error("Importing stack not empty")
            self.log.error(f"{node_stack}")

    def plain_to_tex(self) -> None:
        self.__process_plaintext()
        self.__process_intermediate()

        if not self.object_tree:
            return

        a = QTextCursor(self)
        a.insertText("start")
        j = QTextFrameFormat()
        j.setBorder(2)
        for node in self.object_tree.preorder_traverse():
            print(type(node.data))
            if isinstance(node.data, TerminalMacro):
                print("a")
                a.insertText(node.data.to_text())
            if isinstance(node.data, Environment):
                a.insertFrame(j)
