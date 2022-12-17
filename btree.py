from operator import index
from node import Node
from prob import Prob

class BTree(object):
    def __init__(self, d : int, h : int) -> None:
        self.current_number_of_keys = 0
        self.root = 0
        self.number_of_nodes = 0
        self.node = Node(d, self.number_of_nodes)
        self.number_of_nodes += 1
        self.node.save()
        self.d = d
        self.h = h
        with open('values.data', 'w') as creating_file_for_values:
            pass
        super().__init__()
    
    def print(self, node_index = 0, depth = 0) -> None:
        self.node.load(node_index)
        for children_node_index in self.node.children:
            if children_node_index != -1:
                self.print(children_node_index, depth + 1)
        self.node.load(node_index)
        print("  " * depth, self.node.get_keys_to_print())

    
    def search(self, key: int) -> tuple:
        self.node.load(self.root)
        while True:
            key_index, node_index = self.node.find(key)
            if key_index != -1:
                return True, self.node.dm.get_value(key_index)
            if key_index == -1 and self.node.leaf == 1:
                return False, Prob(-1, -1, -1)
            if key_index == -1 and self.node.leaf != 0:
                if node_index  != -1:
                    self.node.load(node_index)
    
    def split_node(self, xnode : Node, index : int, ynode : Node):
        temp = Node(self.d, self.number_of_nodes + 1)
        self.number_of_nodes += 1
        pass

    def insert(self, key : int, address : int, prob : Prob) -> bool:
        # Already exists
        if self.search(key)[0] or self.current_number_of_keys == (2 * self.d + 1)**self.h - 1:
            return False
        self.node.dm.save_value(address, prob)
        return self._insert(key, address)

    def _insert(self, key : int, address : int, new_child: int = -1) -> bool:
        # Since we called search function, our current node is a leaf
        if self.node.m < 2 * self.d:
        # Insert (x, a) on the current page
            index = 0
            if not key < self.node.keys[0]:
                for i in range(len(self.node.keys)):
                    index += 1
                    if key < self.node.keys[i] or self.node.keys[i] == self.node.max_key:
                        index = i
                        break
            # move all of the keys and addresses to the right
            for j in range(len(self.node.keys)-1, index, -1):
                self.node.keys[j] = self.node.keys[j-1]
                self.node.adds[j] = self.node.adds[j-1]
            self.node.keys[index] = key
            self.node.adds[index] = address
            if new_child != -1:
                for j in range(len(self.node.children)-1, index + 1, -1):
                    self.node.children[j] = self.node.children[j-1]
            self.node.children[index+1] = new_child
                
            self.node.save()
            self.node.m += 1
            return True
        # Will be done after split
        # elif self.node.can_compensate():
        # #Try compensation
        #     return True
        else:
            if self.node.split():
                return True
            else:
                return False

    def full_insert(self, key : int, address : int, new_child: int = -1) -> bool:
        new_node = Node(self.d, self.number_of_nodes, self.node.parent)
        self.number_of_nodes += 1
            
        keys = [x for x in self.node.keys]
        addresses = [x for x in self.node.adds]
        children = [x for x  in self.node.children]

        index = 0
        if not key < keys[0]:
            for i in range(len(keys)):
                index += 1
                if key < keys[i]:
                    index = i
                    break

        
        left_keys = keys[:index]
        right_keys = keys[index:]
        left_addresses = addresses[:index]
        right_addresses = addresses[index:]

        all_keys = left_keys + [key] + right_keys
        all_addresses = left_addresses + [address] + right_addresses

        self.node.children = (2*self.d + 1) * [-1]
        self.node.keys = (2*self.d) * [self.node.max_key]
        self.adds = (2*self.d) * [-1]

        for (i, key) in enumerate(all_keys[:len(all_keys)//2]):
            self.node.keys[i] = key
        
        for (i, add) in enumerate(all_addresses[:len(all_addresses)//2]):
            self.node.addresses[i] = add

        for (i, child) in enumerate(children[:len(children)//2]):
            self.node.children[i] = child

        new_node.children = (2*self.d + 1) * [-1]
        new_node.keys = (2*self.d) * [self.node.max_key]
        new_node.adds = (2*self.d) * [-1]

        for (i, key) in enumerate(all_keys[len(all_keys)//2 + 1:]):
            new_node.keys[i] = key
        
        for (i, add) in enumerate(all_addresses[len(all_addresses)//2 + 1:]):
            new_node.addresses[i] = add

        for (i, child) in enumerate(children[len(children)//2:]):
            new_node.children[i] = child

        if self.parent != -1:
            self.node.save()
            new_node.save()
        else:
            new_root = Node(self.d, self.current_number_of_nodes)
            self.node.parent = self.current_number_of_nodes
            new_node.parent = self.current_number_of_nodes
            self.current_number_of_nodes += 1
            self.node.save()
            new_node.save()
            new_root.save()

        self.node.load(self.parent)
        self._insert(all_keys[len(all_keys)//2 + 1], all_addresses[len(all_addresses)//2 + 1], new_node.index)
           

    def update(self, key: int) -> None:
        pass

    def delete(self, key : int) -> None:
        pass
