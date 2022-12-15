import random
from array import array

def generate_random(size, path='workspace/data.bin'):
    data = []
    for _ in range(size):
        p1 = random.uniform(0, 1)
        p2 = random.uniform(0, 1)
        psum = random.uniform(max(p1,p2), min(p1+p2, 1))
        data.append(p1)
        data.append(p2)
        data.append(psum)
    with open(path, 'wb') as file:
        float_data = array('f', data)
        float_data.tofile(file)
    file.close()

def generate_human(size, path='workspace/data.bin'):
    data = []
    for i in range(size):
        print('{} prawdopodobieństwo, pierwsze: '.format(i+1))
        data.append(float(input()))
        print('drugie: ')
        data.append(float(input()))
        print('suma: ')
        data.append(float(input()))
    with open(path, 'wb') as file:
        float_data = array('f', data)
        float_data.tofile(file)
    file.close()

def from_file(src="test.txt"):
    data = []
    with open(src, 'r') as source:
        lines = source.readlines()
        for line in lines:
            key, p1, p2, psum = line.split(' ')
            data.append(int(key))
            data.append(float(p1))
            data.append(float(p2))
            data.append(float(psum))
    source.close()
    return data
