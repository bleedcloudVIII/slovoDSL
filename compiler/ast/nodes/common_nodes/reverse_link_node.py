from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.word_node import WordNode


class ReverseLinkNode(Node):
    def __init__(self, left: Node, right: Node):
        if not isinstance(left, Node):
            raise Exception("LinkNode: left is not a Node")

        if not isinstance(right, Node):
            raise Exception("LinkNode: right is not a Node")

        self.left = left
        self.right = right

    def execute(self):
        right_value = self.right.execute()

        if isinstance(self.left, WordNode):
            self.left.set(right_value)

    def __str__(self):
        return f"ReverseLinkNode<{self.left}, {self.right}>"

    def __repr__(self):
        return f"ReverseLinkNode<{self.left}, {self.right}>"
