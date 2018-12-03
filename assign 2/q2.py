__author__ = 'Si Yi Wu'

def find_product (l):
    enumerated_l = list(enumerate(l))
    ranges = map(lambda x:(x,x+5),xrange(len(l)-4))
    #print ranges
    list_to_multiply = map(lambda x:(x[0],list(l[x[0]:x[1]])),ranges)
    #print list_to_multiply
    product_list = map(lambda x: (x[0],reduce(lambda a,b : a*b, x[1])), list_to_multiply)
    #print product_list
    max_product = reduce(find_max,product_list)
    #print max_product
    return max_product




#helper function to find the tuple with the largest product
def find_max(a,b):
    return ((a[1] >= b[1]) and a) or ((b[1] > a[1]) and b)





if __name__ == "__main__":
    l = [1,2,3,4,5,6,4,2,1,3]
    print find_product(l)
