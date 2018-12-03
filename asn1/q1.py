__author__ = 'Si Yi Wu'



def gcd (a, b):
     greatestDevider = min(a,b)
     for i in xrange(greatestDevider,0, -1):
         if (a%i == 0) and (b%i == 0):
             return i



