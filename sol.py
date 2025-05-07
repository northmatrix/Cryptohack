from collections import namedtuple
from sympy.ntheory import sqrt_mod

Point = namedtuple("Point", "x y")

B = 1
A = 486662
p = 2**255 - 19

g_x = 9
g_y = sqrt_mod(g_x**3 + 486662 * g_x**2 + g_x, p)
G = Point(g_x, g_y)
print(G)
k = 0x1337C0DECAFE


def montgomery_add(P, Q):
    assert P.x != Q.x or P.y != Q.y
    alpha = (Q.y - P.y) * pow((Q.x - P.x), -1, p)
    alpha %= p
    x = B * (alpha) ** 2 - A - P.x - Q.x
    x %= p
    y = alpha * (P.x - x) - P.y
    y %= p
    return Point(x, y)


def montgomery_double(P):
    alpha = (3 * P.x**2 + 2 * A * P.x + 1) * pow(2 * B * P.y, -1, p)
    alpha %= p
    x = B * alpha**2 - A - 2 * P.x
    x %= p
    y = alpha * (P.x - x) - P.y
    y %= p
    return Point(x, y)


def montgomery_bin(P, k):
    k_bin = bin(k)[2:]  # We extract the bits and remove the prefix "0b"
    k_bin = k_bin[::-1]  # We inverse the bit order to fit the algorithm notation
    l = len(k_bin)
    R0 = P
    R1 = montgomery_double(P)

    for i in range(l - 2, -1, -1):  # We iterate from l-2 to 0
        R0_temp = R0
        R1_temp = R1
        if k_bin[i] == "0":
            R0 = montgomery_double(R0_temp)
            R1 = montgomery_add(R0_temp, R1_temp)
        else:
            R0 = montgomery_add(R0_temp, R1_temp)
            R1 = montgomery_double(R1_temp)
    return R0


print(montgomery_bin(G, k))
