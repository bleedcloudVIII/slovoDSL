from compiler.ast.nodes.node import Node


class AssignNode(Node):
    def __init__(self, variable: Node, expression: Node):
        if not isinstance(expression, Node):
            raise Exception("AssignNode: expression is not Node")

        if variable.is_key_word:
            raise Exception("AssignNode: variable is a key word")

        self.variable_name = variable.token.token_text
        self.expression = expression

    def execute(self):
        # Задаваться значения для переменных будут через LinkNode
        pass

    def __str__(self):
        return f"AssignNode<{self.variable_name}, {self.expression}>"

    def __repr__(self):
        return f"AssignNode<{self.variable_name}, {self.expression}>"
