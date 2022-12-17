from btree import BTree
from node import Node
from prob import Prob
import get_data
address = 0

def test(address):
    tree = BTree(2, 2)
    data = get_data.from_file()
    print(data)
    for i in range(len(data)):
        # testing file has 4 numbers
        # first one is the key used in the tree
        # second, third and fourth are attributes of Prob object
        prob = Prob(data[i][1], data[i][2], data[i][3])
        print("Inserting to a btree -> key {}, Prob: {}".format(data[i][0], prob))
        tree.insert(data[i][0], address, prob)
        address += 1
        tree.print()
    print("search for key 2 = {}".format(tree.search(2)[1]))
    to_update = Prob(0.3, 0.4, 0.1)
    tree.update(2, to_update)
    to_update = Prob(0.3, 0.4, 0.1)
    print("search for key 2 = {}".format(tree.search(2)[1]))

def interactive():
    tree = BTree(2, 2)
    print(48 * "=")
    print("BTREE -> SUPPORTED COMMANDS: ADD, DELETE, FIND, PRINT")
    print(48 * "=")
    while True:
        command = str(input())

        break


if __name__ == '__main__':
    test(address)
    #interactive()


