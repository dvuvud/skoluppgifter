def double(n):
    return n*2
def triple(n):
    return n*3
def quadruple(n):
    return double(double(n))
def funky(n, m):
    return triple(n) + quadruple(m)

a = 3
b = 14

d1 = double(a)       # 6
d2 = double(b)       # 28

t1 = triple(a)       # 9
t2 = triple(b)       # 42

q1 = quadruple(a)    # 12
q2 = quadruple(b)    # 56

f1 = funky(a, b)     # 65
f2 = funky(b, b)     # 98