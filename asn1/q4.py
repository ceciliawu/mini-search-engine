__author__ = 'Si Yi Wu'

import math


def factorize(N):
    """
    doctest cases:
    >>> factorize(6)
    [1, 2, 3]
    >>> factorize (225)
    [1, 3, 3, 5, 5]
    >>> factorize (51)
    [1, 3, 17]
    >>> factorize (24)
    [1, 2, 2, 2, 3]
    >>> factorize (13)
    [1, 13]

    """

    l = []
    l.append(1)
    for i in (xrange(2, int(math.ceil(math.sqrt(N)))+1,1)):
        while (N % i == 0):
            l.append(i)
            N = N/i
    #in case the left N is not 1 ( a prime number)
    if N != 1:
        l.append(N)
    l.sort()
    return l



if __name__ == "__main__":
    import doctest
    doctest.testmod()