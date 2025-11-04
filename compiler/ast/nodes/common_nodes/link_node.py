from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.word_node import WordNode


class LinkNode(Node):
    def __init__(self, left_token: Node, right_token: Node):
        # TODO Проверки
        self.left_token = left_token
        self.right_token = right_token

    def execute(self):
        left_value = self.left_token.execute()

        if isinstance(self.right_token, WordNode):
            self.right_token.set(left_value)
