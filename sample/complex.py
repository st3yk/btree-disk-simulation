class ComplexNum(object):
    def __init__(self, real, imag) -> None:
        self.real = real
        self.imag = imag
        self.module = (self.real ** 2 + self.imag ** 2) ** 0.5
    
    def __str__(self) -> str:
        if self.imag >= 0:
            return '{:.3f}+{:.3f}i  {:.3f}'.format(self.real, self.imag, self.module)
        return '{:.3f}{:.3f}i  {:.3f}'.format(self.real, self.imag, self.module)
    
    def __le__(self, other):
        if isinstance(other, ComplexNum):
            return self.module <= other.module
        return NotImplemented