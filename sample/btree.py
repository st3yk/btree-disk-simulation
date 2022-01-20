from node import Node

class BTree(object):
    def __init__(self, d : int, h : int) -> None:
        self.root = 0
        self.node = Node(d, True)
        self.d = d
        self.h = h
        super().__init__()
    
    def _load_node(self):
        pass
    
    def search(self, key: int):
        current_node = self.load_node(self.root)
        current_node.search(key)
        pass
    
    def split_node(self, xnode : Node, index : int, ynode : Node):
        pass

    def insert(self, key : int) -> None:
        pass

    def update(self, key: int) -> None:
        pass

    def delete(self, key : int) -> None:
        pass
