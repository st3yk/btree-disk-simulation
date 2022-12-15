from btree import BTree
from node import Node
from prob import Prob
import get_data

def test():
    tree = BTree(2, 2)
    data = get_data.from_file()
    print(data)
    for i in range(len(data)):
        # testing file has 4 numbers
        # first one is the key used in the tree
        # second, third and fourth are attributes of Prob object
        print(data[i][0])
        address = i
        prob = Prob(data[i][1], data[i][2], data[i][3])
        tree.insert(data[i][0], address, prob)
        tree.print()

if __name__ == '__main__':
    test()
    # tree.node.keys = [1, 3, 5, 7, 10, 123, 150, 200]
    # tree.node.save()
    # tree.print()
    # print(tree.search(5))


