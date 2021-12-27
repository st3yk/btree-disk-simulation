from node import Node

class BTree(object):
    def __init__(self, root : Node, t) -> None:
        self.t = t
        super().__init__()