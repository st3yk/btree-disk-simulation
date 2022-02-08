from array import array
from complex import ComplexNum
import struct

class DiskManager(object):
    def __init__(self, d) -> None:
        self.p_read = 0
        self.p_write = 0
        self.v_read = 0
        self.v_write = 0
        self.pages_path = 'pages.data'
        self.values_path = 'values.data'
        self.page_size = 4 * (1 + 1 + 1 + (2 * d + 1) + (2 * d) + (2 * d))
        super().__init__()
    
    def load_page(self, index) -> list:
        self.p_read += 1
        with open(self.pages_path, 'rb') as pages:
            pages.seek(index * self.page_size)
            data = pages.read(self.page_size)
        pages.close()
        return list(array('i', data))

    def save_page(self, index : int, data : list) -> None:
        self.p_write += 1
        with open(self.pages_path, 'wb') as pages:
            pages.seek(index * self.page_size)
            byte_data = array('i', data)
            byte_data.tofile(pages)
        pages.close()
    
    def get_value(self, address : int) -> ComplexNum:
        self.v_read += 1
        with open(self.values_path, 'rb') as values:
            values.seek(address * 8)
            real = values.read(4)
            imag = values.read(4)
        values.close()
        return ComplexNum(struct.unpack('f', real)[0], struct.unpack('f', imag)[0])

