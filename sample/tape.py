import os
import struct
from complex import ComplexNum
from array import array

class Tape(object):
    def __init__(self, path):
        self.path = path
        self.buffer_size = 40
        self.disk_w = 0
        self.disk_r = 0
        self._ptr = 0
        self.size = 0
        self._toread = []
        self._towrite = []
        if os.path.isfile(self.path):
            self.size = os.path.getsize(self.path)
        self.len = int(self.size / 8)
    
    def clc(self, delete=True):
        if os.path.isfile(self.path):
            if delete:
                os.remove(self.path)
            else:
                self.len = int(os.path.getsize(self.path) / 8)
        self._ptr = 0
        self._toread = []
        self._towrite = []
    
    def is_empty(self):
        if os.path.isfile(self.path):
            self.size = os.path.getsize(self.path)
        return self._ptr == self.size
    
    def print_tape(self):
        if not os.path.isfile(self.path):
            print(self.path, ': (empty)')
            return
        self.len = int(os.path.getsize(self.path) / 8)
        print(self.path)
        i = 0
        with open(self.path, 'rb') as file:
            file.seek(0)
            for _ in range(self.len):
                real = file.read(4)
                imag = file.read(4)
                c = ComplexNum(struct.unpack('f', real)[0], struct.unpack('f', imag)[0])
                print('index {}: {}'.format(i, c)) 
                i += 1
        file.close()
    
    def can_read(self):
        return not (len(self._toread) == 0 and self.is_empty())

    def readt(self) -> ComplexNum:
        if len(self._toread) == 0:
            self._read()
        return self._toread.pop(0)
    
    def _read(self):
        self.disk_r += 1
        if self.is_empty():
            print("End of tape! Error")
            return -1
        self.size = os.path.getsize(self.path)
        nums = []
        with open(self.path, 'rb') as file:
            file.seek(self._ptr)
            for _ in range(int(self.buffer_size / 8)):
                if self._ptr == self.size:
                    break
                real = file.read(4)
                imag = file.read(4)
                c = ComplexNum(struct.unpack('f', real)[0], struct.unpack('f', imag)[0])
                nums.append(c)
                self._ptr += 8
        file.close()
        self._toread = nums
    
    def close(self):
        self._write()
    
    def write(self, num):
        self._towrite.append(num)
        if len(self._towrite) * 8 == self.buffer_size:
            self._write()
            self._towrite = []

    def _write(self):
        self.disk_w += 1
        data = []
        for num in self._towrite:
            data.append(num.real)
            data.append(num.imag)
        with open(self.path, 'ab') as file:
            float_data = array('f', data)
            float_data.tofile(file)
        file.close()
