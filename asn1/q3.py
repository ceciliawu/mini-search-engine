__author__ = 'Si Yi Wu'

cache = {}
def fib (n,l):
    l.append(n)
    if n in cache:
        return cache[n]
    if n in [0,1]:
        result = n
    else:
        result = fib (n-1,l) + fib (n-2,l)
        cache[n] = result
    return result

