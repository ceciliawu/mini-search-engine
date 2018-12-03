__author__ = 'Si Yi Wu'

from time import clock

PROFILE_FUNCTIONS = True
PROFILE_RESULTS = {}

def profile (fn):
    def profiled_fn (*args,**kwargs):
        if PROFILE_FUNCTIONS:
            start = clock()
            fn(*args,**kwargs)
            duration = clock() - start
            if fn.__name__ not in PROFILE_RESULTS:
                PROFILE_RESULTS[fn.__name__] = (duration,1)
            else:
                total_num = PROFILE_RESULTS[fn.__name__][1]+1
                avg_time = (PROFILE_RESULTS[fn.__name__][0] + duration)/(total_num)
                PROFILE_RESULTS[fn.__name__] = (avg_time,total_num)
        else:
            fn(*args,**kwargs)
    return profiled_fn



@profile
def f1( a ):
    i = 0
    for j in xrange(25):
        i += a
    print "f1"
    print i


@profile
def f2():
    i = 0
    for j in xrange(5):
        i += 1
    print "f2:"
    print i


@profile
def f3(a=1,b=1):
    print "f3:"
    print a
    print b
    i = 0
    for j in xrange(10):
        i += a
    print i

if __name__ == "__main__":
    f1(3)
    f1(2)
    f1(5)
    f2()
    f3(a=2)
    print PROFILE_RESULTS