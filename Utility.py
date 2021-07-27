from functools import reduce

def bind(f, li):
    return reduce(lambda a,b: a+b, map(f, li))
