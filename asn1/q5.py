__author__ = 'Si Yi Wu'

import math
C = 50
H = 30

def Q (D):
    return [int(math.sqrt((2*C*d)/H)) for d in D]
