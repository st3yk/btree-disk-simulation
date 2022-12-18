from operator import index
from node import Node
from prob import Prob

class BTree(object):
    def __init__(self, d : int, h : int) -> None:
        with open('values.data', 'w') as creating_file_for_values:
            pass
        with open('pages.data', 'w') as creating_file_for_pages:
            pass
        self.current_number_of_keys = 0
        self.root = 0
        self.number_of_nodes = 0
        self.node = Node(d, self.number_of_nodes)
        self.number_of_nodes += 1
        self.node.save()
        self.d = d
        self.h = h
        super().__init__()
    
    def print(self) -> None:
        self.node.load(self.root)
        self.node.print()
    
    def search(self, key: int, get_address : bool = False) -> tuple:
        self.node.load(self.root)
        while True:
            key_index, node_index = self.node.find(key)
            if key_index != -1:
                if get_address:
                    return True, self.node.dm.get_value(self.node.adds[key_index]), self.node.adds[key_index]
                else:
                    return True, self.node.dm.get_value(self.node.adds[key_index])
            if key_index == -1 and self.node.leaf == 1:
                return False, Prob(-1, -1, -1)
            if key_index == -1 and self.node.leaf != 0:
                if node_index  != -1:
                    self.node.load(node_index)

    def insert(self, key : int, address : int, prob : Prob) -> bool:
        # Already exists
        if self.search(key)[0] or self.current_number_of_keys == (2 * self.d + 1)**self.h - 1:
            print('Key {} already exists in the tree or current number of keys = max keys'.format(key))
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
                
            self.node.m += 1
            self.node.save()
            return True
        elif self._compensate_insert(key, address):
            return True
        else:
            return self._split_insert(key, address, new_child)

    def _compensate_insert(self, key : int, address : int, new_child : int = -1) -> bool:
        if new_child != -1:
            return False
        current = self.node.index
        # You have to find your index in parent's children list
        # keys[your-1] -> left sibling
        # keys[your+1] -> right sibling
        # If there is no parent we cannot compensate
        if self.node.parent != -1:
            self.node.load(self.node.parent)
            print('PERFORMING COMPENSATION, PARENT\'S KEYS: {}'.format(self.node.keys))
            try:
                index_in_parent = self.node.children.index(current)
            except:
                index_in_parent = -1
            left_sibling = -1
            right_sibling = -1
            if index_in_parent > 0:
                left_sibling = self.node.children[index_in_parent - 1]
                print('LEFT SIBLING: {}'.format(left_sibling))
                parent_left_key = self.node.keys[index_in_parent-1]
                parent_left_add = self.node.adds[index_in_parent-1]
            if index_in_parent != self.d * 2:
                right_sibling = self.node.children[index_in_parent + 1]
                print('RIGHT SIBLING: {}'.format(right_sibling))
                parent_right_key = self.node.keys[index_in_parent]
                parent_right_add = self.node.adds[index_in_parent]
            # Try left sibling first
            if left_sibling != -1:
                self.node.load(left_sibling)
                if self.node.m < self.d * 2:
                    # Add parent key as the last element in the sibling
                    self.node.keys[self.node.m] = parent_left_key
                    self.node.adds[self.node.m] = parent_left_add
                    self.node.m += 1
                    self.node.save()
                    # Insert (x, a) on the current page
                    self.node.load(current)
                    if key < self.node.keys[0]:
                    # add key to parent, no need for modyfing self.node.keys
                        self.node.load(self.node.parent)
                        self.node.keys[index_in_parent-1] = key
                        self.node.adds[index_in_parent-1] = address
                        self.node.save()
                        if self.node.verbose:
                            print('DONE COMPENSATION')
                        return True
                    else:
                        to_parent_key = self.node.keys[0]
                        to_parent_add = self.node.adds[0]
                        self.node.keys = self.node.keys[1:] + [self.node.max_key]
                        self.node.adds = self.node.adds[1:] + [-1]
                        # insert key on the current page
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
                        self.node.save()
                        # Add to_parent
                        self.node.load(self.node.parent)
                        self.node.keys[index_in_parent-1] = to_parent_key
                        self.node.adds[index_in_parent-1] = to_parent_add
                        self.node.save()
                        if self.node.verbose:
                            print('DONE COMPENSATION')
                        return True
            if right_sibling != -1:
                self.node.load(right_sibling)
                if self.node.m < self.d * 2:
                    # Add parent key as the first element in the sibling
                    self.node.keys = [parent_right_key] + self.node.keys[:-1]
                    self.node.adds = [parent_right_add] + self.node.adds[:-1]
                    self.node.m += 1
                    self.node.save()
                    # Insert (x, a) on the current page
                    self.node.load(current)
                    if key > self.node.keys[self.node.m-1]:
                    # add key to parent, no need for modyfing self.node.keys
                        self.node.load(self.node.parent)
                        self.node.keys[index_in_parent] = key
                        self.node.adds[index_in_parent] = address
                        self.node.save()
                        if self.node.verbose:
                            print('DONE COMPENSATION')
                        return True
                    else:
                        to_parent_key = self.node.keys[self.node.m-1]
                        to_parent_add = self.node.adds[self.node.m-1]
                        self.node.keys[self.node.m-1] = self.node.max_key
                        self.node.adds[self.node.m-1] = -1
                        # insert key on the current page
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
                        self.node.save()
                        # Add to_parent
                        self.node.load(self.node.parent)
                        self.node.keys[index_in_parent] = to_parent_key
                        self.node.adds[index_in_parent] = to_parent_add
                        self.node.save()
                        if self.node.verbose:
                            print('DONE COMPENSATION')
                        return True
        self.node.load(current)
        return False

    def _split_insert(self, key : int, address : int, new_child: int = -1) -> bool:
        if self.node.verbose:
            print('PERFORMING SPLIT')
        new_node = Node(self.d, self.number_of_nodes, self.node.leaf, self.node.parent)
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
        if new_child != -1:
            tmp_children = children[:index+1] + [new_child] + children[index+1:]
            children = tmp_children

        self.node.children = (2*self.d + 1) * [-1]
        self.node.keys = (2*self.d) * [self.node.max_key]
        self.node.adds = (2*self.d) * [-1]

        for (i, k) in enumerate(all_keys[:len(all_keys)//2]):
            self.node.keys[i] = k
        
        for (i, add) in enumerate(all_addresses[:len(all_addresses)//2]):
            self.node.adds[i] = add

        current_node_index = self.node.index
        for (i, child) in enumerate(children[:len(children)//2]):
            child_node = Node(self.d, child)
            self.node.children[i] = child
            if child != -1:
                child_node.load(child)
                child_node.parent = current_node_index
                child_node.save()

        new_node.children = (2*self.d + 1) * [-1]
        new_node.keys = (2*self.d) * [self.node.max_key]
        new_node.adds = (2*self.d) * [-1]

        if self.node.verbose:
            print('ALL OF THE KEYS TO SPLIT {}'.format(all_keys))
        for (i, k) in enumerate(all_keys[len(all_keys)//2 + 1:]):
            new_node.keys[i] = k
        if self.node.verbose:
            print('KEYS THAT WILL GO TO THE LEFT {}'.format(self.node.get_keys_to_print()))
            print('KEYS THAT WILL GO TO THE RIGHT {}'.format(new_node.get_keys_to_print()))
        
        for (i, add) in enumerate(all_addresses[len(all_addresses)//2 + 1:]):
            new_node.adds[i] = add

        new_node_index = new_node.index
        for (i, child) in enumerate(children[len(children)//2:]):
            child_node = Node(self.d, child)
            new_node.children[i] = child
            if child != -1:
                child_node.load(child)
                child_node.parent = new_node_index
                child_node.save()

        if self.node.parent != -1:
            self.node.m = self.d
            new_node.m = self.d
            self.node.parent = self.node.parent
            new_node.parent = self.node.parent
            self.node.save()
            new_node.save()
            self.node.load(self.node.parent)
            return self._insert(all_keys[len(all_keys)//2], all_addresses[len(all_addresses)//2], new_node.index)
        else:
            new_root = Node(self.d, self.number_of_nodes, -1)
            self.root = self.number_of_nodes
            new_root.children[0] = self.node.index
            new_root.keys[0] = all_keys[len(all_keys)//2]
            new_root.adds[0] = all_addresses[len(all_addresses)//2]
            new_root.children[1] = new_node.index
            self.node.parent = self.number_of_nodes
            new_node.parent = self.number_of_nodes
            self.node.m = self.d
            new_node.m = self.d
            new_root.m = 1
            self.number_of_nodes += 1
            self.node.save()
            new_node.save()
            new_root.save()
            return True

    def update(self, key: int, new : Prob) -> bool:
        wasFound = self.search(key, True)
        if wasFound[0]:
            address = wasFound[2]
            if self.node.verbose:
                print('Key {} was found at the address {}, value: {}'.format(key, address, str(wasFound[1])))
                print('Updating address {} with value: {}'.format(address, str(new)))
            self.node.dm.update_value(address, new)
            return True
        else:
            if self.node.verbose:
                print('Key {} was not found in the tree.'.format(key))
            return False
            

