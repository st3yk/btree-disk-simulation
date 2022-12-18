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
        if tree.insert(data[i][0], address, prob):
            address += 1
        tree.print()
    print("search for key 2 = {}".format(tree.search(2)[1]))
    tree.update(2, Prob(0.3, 0.4, 0.1))
    print("search for key 2 = {}".format(tree.search(2)[1]))
    print("search for key 421 = {}".format(tree.search(421)[1]))
    tree.update(421, Prob(0.5, 0.1, 0.05))
    print("search for key 421 = {}".format(tree.search(421)[1]))

def interactive(address):
    tree = BTree(2, 2)
    print(60 * "=")
    print("BTREE -> SUPPORTED COMMANDS: ADD, UPDATE, FIND, PRINT, EXIT")
    print(60 * "=")
    while True:
        print("NEXT COMMAND:")
        command = str(input())
        if command == "ADD" or command == "A":
            print("[INSERT] {Key p1 p2 psum}")
            i = input().split()
            key, p1, p2, psum = int(i[0]), float(i[1]), float(i[2]), float(i[3])
            if tree.insert(key, address, Prob(p1, p2, psum)):
                address += 1
        elif command == "UPDATE" or command == "U":
            print("[UPDATE] {Key p1 p2 psum}")
            i = input().split()
            key, p1, p2, psum = int(i[0]), float(i[1]), float(i[2]), float(i[3])
            tree.update(key, Prob(p1, p2, psum))
        elif command == "FIND" or command == "F":
            print("[FIND] Key:")
            key = int(input())
            wasFound = tree.search(key, True)
            if wasFound[0]:
                address = wasFound[2]
                print('Key {} was found at the address {}, value: {}'.format(key, address, str(wasFound[1])))
            else:
                print('Key {} was not found in the tree.'.format(key))
        elif command == "PRINT" or command == "P":
            tree.print()
        elif command == "EXIT" or command == "E":
            tree.print()
            print('EXITING')
            break
        else:
            print("COMMAND NOT RECOGNIZED")

if __name__ == '__main__':
    #test(address)
    interactive(address)


