__author__ = 'Si Yi Wu'

def my_map(func,list):
    if (func is None) or (not list):
        return list
    return_list = []
    for i in list:
        return_list.append(func(i))
    return return_list


def my_reduce(func,list):
    if (func is None) or (not list):
        return list
    result = list[0]
    for e in list[1:]:
        result = func (result,e)
    return result

def my_filter(func,list):
    if (func is None) or (not list):
        return list
    return_list = []
    for e in list:
        if (func(e)):
            return_list.append(e)
    return return_list

if __name__ == "__main__":
    print my_map(None, [1,2,3])
    print my_map(lambda x: x * x , [1,2,3])

    print my_reduce(lambda x,y:x*y,[1,2,3,4])

    print my_filter((lambda x: x < 0), range(-5,5))