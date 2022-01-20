from btree import BTree
from node import Node


if __name__ == '__main__':
    r = Node(2)
    print(len(r.children))
    print(len(r.keys))
