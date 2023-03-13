from typing import Optional, Union
from latex import build_pdf
from pathlib import Path
from PyQt6.QtGui import QTextDocument, QTextCursor, QTextFrameFormat
from PyTeXEditor.extract_latex import seperate
from PyTeXEditor.data_structures import Tree, Node
from PyTeXEditor.document_elements import (
    Block,
    Environment,
    TerminalMacro,
    IncludeTerminator,
    ENVIRONMENTS,
    MACROS,
    Document
)
import logging


class LatexDocument(QTextDocument):
    log = logging.getLogger("LatexDocument")

    def __init__(self):
        self.plain_text: list[str] = list()
        self.intermediate: list[str] = list()
        self.object_tree: Optional[Tree[Block]] = None
        super().__init__()

    def big_brain_traverse(self, node: Optional[Node[Block]] = None
                           ) -> list[Union[Node[Block], str]]:
        """_summary_

        Parameters
        ----------
        node : Node[Block] | None, optional
            _description_, by default None

        Returns
        -------
        list[Node[Block] | str]
            List of nodes with the end of an environemnt shown with a string
            with the name of the environment.

        Raises
        ------
        RuntimeError
            When the `object_tree` is empty.
        TypeError
            When a node that is neither an `Environment` or `Macro`
        """
        if not node:
            if self.object_tree:
                node = self.object_tree.root
            else:
                raise RuntimeError("What the")
        if isinstance(node.data, TerminalMacro):
            return [node]
        if isinstance(node.data, Environment):
            output: list[Node[Block] | str] = [node]
            for children in node.children:
                output += self.big_brain_traverse(children)

            output.append(node.data.name)
            return output
        raise TypeError("What the?")

    def __process_plaintext(self) -> None:
        self.intermediate = seperate(self.plain_text)

    def __process_intermediate(self) -> None:

        if not self.intermediate:
            self.log.error("intermediate is empty")
            return None

        doc_begin = Document.initiator

        i = 0
        id_counter: int = 0
        # Scans the intermediate to get to the begin{document} macro
        while len(self.intermediate) > i:
            if doc_begin.match(self.intermediate[i]):
                # Starts the tree if the document is found
                root_object = Node[Block](
                    id_counter, Document()
                )
                self.object_tree = Tree[Block](root_object)
                root_object.data.process_data(
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

            for macro_type in MACROS:
                regex = macro_type.initiator
                if regex.match(self.intermediate[i]):
                    self.log.debug(f"Element is {macro_type}")
                    new_node = Node[Block](
                        id_counter, macro_type()
                    )
                    node_stack[-1].add_child(new_node)
                    node_stack.append(new_node)
                    # Don't add to stack

            for env_type in ENVIRONMENTS:
                regex = env_type.initiator
                if regex.match(self.intermediate[i]):
                    self.log.debug(f"Element is {env_type.name}")
                    new_node = Node[Block](
                        id_counter,
                        env_type()
                    )
                    node_stack[-1].add_child(new_node)
                    node_stack.append(new_node)

            i += 1

        if node_stack:
            self.log.error("Importing stack not empty")
            self.log.error(f"{node_stack}")

    def plain_to_tex(self) -> None:  # pragma: no cover
        self.__process_plaintext()
        self.__process_intermediate()

    def internal_to_qt(self) -> None:

        if not self.object_tree:
            return None

        cursor = QTextCursor(self)

        for current_node in self.big_brain_traverse(self.object_tree.root):

            if isinstance(current_node, str):
                # End of environment
                cursor.movePosition(QTextCursor.MoveOperation.NextBlock,
                                    QTextCursor.MoveMode.MoveAnchor)
                continue

            if isinstance(current_node.data, Environment):
                print(f"Env: {type(current_node.data)}")

                # == TEST ==
                frame = QTextFrameFormat()
                frame.setBorder(3)
                # == TEST ==

                cursor.insertFrame(frame)

            elif isinstance(current_node.data, TerminalMacro):
                cursor.insertText(current_node.data.to_plain())
                print(f"OUT: '{current_node.data.to_plain()}'")

    def compile(self, tex_path: Path) -> None:
        pdf_name = f"{tex_path.stem}.pdf"
        pdf_data = build_pdf(open(tex_path))
        pdf_data.save_to(pdf_name)
