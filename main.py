from btree import BTree
from node import Node
import get_data

def test():
    tree = BTree(2, 2)
    data = get_data.from_file()
    for address in range(data):
        # For now I only operate on key - data[i][0] and address
        # FIXME implement adding Prob objects to values.bin
        print(data[i][0])
        tree.insert(data[i][0], address)

if __name__ == '__main__':
    test()
    # tree.node.keys = [1, 3, 5, 7, 10, 123, 150, 200]
    # tree.node.save()
    # tree.print()
    # print(tree.search(5))


