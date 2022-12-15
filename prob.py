class Prob(object):
    def __init__(self, p1, p2, psum) -> None:
        self.p1 = p1
        self.p2 = p2
        self.psum = psum
        self.pprod = self.p1 + self.p2 - self.psum
    
    def __str__(self) -> str:
        return 'p1={:.3f} p2={:.3f} sum={:.3f} prod={:.3f}'.format(self.p1, self.p2, self.psum, self.pprod)
    
    def __le__(self, other):
        if isinstance(other, Prob):
            return self.pprod <= other.pprod
        return NotImplemented