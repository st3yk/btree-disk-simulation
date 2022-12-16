from array import array
from prob import Prob
import struct

class DiskManager(object):
    def __init__(self, d) -> None:
        self.p_read = 0
        self.p_write = 0
        self.v_read = 0
        self.v_write = 0
        self.pages_path = 'pages.data'
        self.values_path = 'values.data'
        # m - current number of keys, pointer to parent, am I leaf?, children, keys, addresses - each of these 4 bytes
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
    
    def get_value(self, address : int) -> Prob:
        self.v_read += 1
        with open(self.values_path, 'rb') as values:
            values.seek(address * 12)
            p1 = values.read(4)
            p2 = values.read(4)
            psum = values.read(4)
        values.close()
        return Prob(struct.unpack('f', p1)[0], struct.unpack('f', p2)[0], struct.unpack('f', psum)[0])
    
    def save_value(self, address, prob : Prob) -> None:
        self.v_write += 1
        with open(self.values_path, 'ab') as values:
            values.seek(address * 12)
            to_write = array('f', [prob.p1, prob.p2, prob.psum])
            to_write.tofile(values)
        values.close()

