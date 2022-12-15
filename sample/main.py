from btree import BTree
from node import Node


if __name__ == '__main__':
    tree = BTree(4, 2)
    tree.node.keys = [1, 3, 5, 7, 10, 123, 150, 200]
    tree.node.save()
    tree.print()
    print(tree.search(5))


