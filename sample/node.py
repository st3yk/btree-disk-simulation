from complex import ComplexNum
from diskmanager import DiskManager

class Node(object):
    def __init__(self, d : int, leaf=0) -> None:
        # This is to be used for any node
        self.index = -1
        self.d = d
        self.dm = DiskManager(d)

        # Save this in page
        # m = current number of keys on the page
        self.m = 0
        self.parent = -1
        self.leaf = leaf 
        self.children = (2*d + 1) * [-1]
        self.keys = (2*d) * [0]
        super().__init__()
    
    def load(self, index: int) -> None:
        self.index = index
        data = self.dm.load_page(index)

        self.m = data.pop(0)
        self.leaf = data.pop(0)
        self.parent = data.pop(0)
        for i in range(2 * self.d):
            self.children[i] = data.pop(0)
            self.keys[i] = data.pop(0)
        self.children[-1] = data.pop(0)

    def save(self) -> None:
        data = []
        data.append(self.m)
        data.append(self.leaf)
        data.append(self.parent)
        for i in range(2 * self.d):
            data.append(self.children[i])
            data.append(self.keys[i])
        data.append(self.children[-1])
        self.dm.save_page(self.index, data)
