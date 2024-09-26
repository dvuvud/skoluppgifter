def double(n):
    return n*2

def triple(n):
    return n*3

def quadruple(n):
    return n*4

def funky(n, m):
    return triple(n) + quadruple(m)

a = 3
b = 14

print(double(a))       # 6
print(double(b))       # 28

print(triple(a))       # 9
print(triple(b))       # 42

print(quadruple(a))    # 12
print(quadruple(b))    # 56

print(funky(a, b))     # 65
print(funky(b, b))     # 98