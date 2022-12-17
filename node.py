from diskmanager import DiskManager
from prob import Prob

class Node(object):
    def __init__(self, d : int, index: int, leaf=1, parent=-1) -> None:
        self.max_key = 2147483646
        # If you want to print info, otherwise set to False
        self.verbose = True
        # This is to be used for any node
        self.index = index
        self.d = d
        self.dm = DiskManager(d)
        # Save this in page
        # m = current number of keys on the page
        self.m = 0
        # Every newly created Node is a leaf
        self.leaf = leaf
        self.parent = parent
        self.children = (2*d + 1) * [-1]
        self.keys = (2*d) * [self.max_key]
        self.adds = (2*d) * [-1]
        super().__init__()
    
    def load(self, index: int) -> None:
        self.index = index
        data = self.dm.load_page(index)
        self.m = data.pop(0)
        self.leaf = data.pop(0)
        self.parent = data.pop(0)
        self.children[0] = data.pop(0)
        for i in range(2 * self.d):
            self.keys[i] = data.pop(0)
            self.adds[i] = data.pop(0)
            self.children[i+1] = data.pop(0)
    
    def get_keys_to_print(self) -> list:
        to_print = []
        for key in self.keys:
            if key < self.max_key:
                to_print.append(key)
            else:
                to_print.append("empty")
        return to_print

    def save(self) -> None:
        data = []
        data.append(self.m)
        data.append(self.leaf)
        data.append(self.parent)
        data.append(self.children[0])
        for i in range(2 * self.d):
            data.append(self.keys[i])
            data.append(self.adds[i])
            data.append(self.children[i+1])
        print('saving node: {}, parent: {}'.format(self.index, self.parent))
        print(data)
        self.dm.save_page(self.index, data)
    
    def find(self, key : int) -> int:
        low = 0
        high = len(self.keys) - 1
        key_index = 0
        while low <= high:
            key_index = (high + low) // 2
            if self.keys[key_index] < key:
                low = key_index + 1
            elif self.keys[key_index] > key:
                high = key_index - 1
            else:
                if self.verbose:
                    print("Found key {} at index {}, address = {}".format(key, key_index, self.adds[key_index]))
                return key_index, -1
        if key < self.keys[key_index]:
            if self.verbose:
                print("Not found {}, finished at [{}]: {}, LEFT".format(key, key_index, self.keys[key_index]))
            return -1, self.children[key_index]
        else:
            if self.verbose:
                print("Not found {}, finished at [{}]: {}, RIGHT".format(key, key_index, self.keys[key_index]))
            return -1, self.children[key_index + 1]

    def print(self, depth=0) -> None:
        print("  " * depth, "{}, parent: {}".format(self.get_keys_to_print(), self.parent))
        for child_node_index in self.children:
            if child_node_index != -1:
                child_node = Node(self.d, child_node_index)
                child_node.load(child_node_index)
                child_node.print(depth + 1)
    