

def hailstone(n):
    """Print out the hailstone sequence starting at n, and return the
    number of elements in the sequence.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    "*** YOUR CODE HERE ***"
    if n == 1:
        print(n)
        return 1
    elif n % 2 == 0:
        print(n)
        result = 1 + hailstone(n // 2)
    else:
        print(n)
        result = 1 + hailstone(n * 3 + 1)
    return result

def symmetric(l):
    """Returns whether a list is symmetric. 
    >>> symmetric([])
    True
    >>> symmetric([1])
    True
    >>> symmetric([1, 4, 5, 1])
    False
    >>> symmetric([1, 4, 4, 1])
    True
    >>> symmetric(['l', 'o', 'l'])
    True
    """
    "*** YOUR CODE HERE ***"
    n = len(l)
    if n <= 1:
        return True
    else :
        return symmetric(l[1:-1]) and l[0] == l[-1]
    '''elif n % 2 == 0:
        return symmetric(l[:n//2-1]+l[-n//2+1:]) and l[n//2-1] == l[-n//2]
'''
