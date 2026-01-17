from compiler.ast.nodes.node import Node


class PathNode(Node):
    def __init__(self, path: str):
        self.path = path

    def execute(self):
        return None

    def __str__(self):
        return f"PathNode<{self.path}>"

    def __repr__(self):
        return f"PathNode<{self.path}>"
