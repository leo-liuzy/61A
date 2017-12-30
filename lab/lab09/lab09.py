# Q1
class ScaleIterator:
    """An iterator the scales elements of the iterable s by a number k.

    >>> s = ScaleIterator([1, 5, 2], 5)
    >>> for elem in s:
    ...     print(elem)
    5
    25
    10
    >>> m = ScaleIterator([1, 2, 3, 4, 5, 6], 2)
    >>> [next(m) for _ in range(5)]
    [2, 4, 6, 8, 10]
    """
    def __init__(self, s, k):
        self.lst = s
        self.scales = k
        self.current = 0
        self.step = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.lst):
            raise StopIteration
        val = self.lst[self.current] * self.scales
        self.current += self.step
        return val
