class DiskManager(object):
    def __init__(self, d) -> None:
        self.read = 0
        self.write = 0
        self.path = 'pages.data'
        self.pagesize = 4 * (1 + 1 + 1 + (2 * self.d + 1) + (2 * self.d))
        super().__init__()
    
    def load_page(self, index) -> list:
        self.read += 1
        with open(self.path, 'rb') as file:
            file.seek(index * self.pagesize)
            data = file.read(self.pagesize)
        file.close()
        return data

    def save_page(self, index : int, data : list) -> None:
        self.write += 1
        with open(self.path, 'wb') as file:
            file.seek(index * self.pagesize)
            file.write(data)
        file.close()
