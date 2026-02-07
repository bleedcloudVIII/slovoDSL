from compiler.ast.nodes.node import Node


class ListNode(Node):
    def __init__(self, expressions: list[Node]):
        if not isinstance(expressions, list):
            raise Exception("AssignNode: expression is not Node")

        self.expressions = expressions

    def execute(self):
        pass

    def __str__(self):
        return f"ListNode<count: {len(self.expressions)}>"

    def __repr__(self):
        return f"ListNode<count: {len(self.expressions)}>"
