from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import pad, unpad
from collections import namedtuple
from random import randint
import hashlib
from sympy import ntheory
from sympy.ntheory.qs import log


Point = namedtuple("Point", "x y")
O = "Origin"

# Define the curve
p = 310717010502520989590157367261876774703
a = 2
b = 3

# Generator
g_x = 179210853392303317793440285562762725654
g_y = 105268671499942631758568591033409611165
G = Point(g_x, g_y)


# Bob's public key
b_x = 272640099140026426377756188075937988094
b_y = 51062462309521034358726608268084433317
B = Point(b_x, b_y)


def check_point(P: tuple):
    if P == O:
        return True
    else:
        return (
            (P.y**2 - (P.x**3 + a * P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p
        )


def point_inverse(P: tuple):
    if P == O:
        return P
    return Point(P.x, -P.y % p)


def point_addition(P: tuple, Q: tuple):
    # based of algo. in ICM
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3 * P.x**2 + a) * inverse(2 * P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam * (P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    assert check_point(R)
    return R


def double_and_add(P: tuple, n: int):
    # based of algo. in ICM
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2
    assert check_point(R)
    return R


# We will calculate the order using external tool sage
#
# p = 310717010502520989590157367261876774703
# a = 2
# b = 3
#
# E = EllipticCurve(GF(p),[a,b])
# print(E.order())
#
#
# 310717010502520989590206149059164677804
order = 310717010502520989590206149059164677804
factors = ntheory.factorint(order)
x = max(factors)
print(log(x, 2))


# Smooth factors so it can be easily factored we will use built in sage discrete_log

#
# p = 310717010502520989590157367261876774703
# a = 2
# b = 3
#
# E = EllipticCurve(GF(p),[a,b])
#
# # Generator
# g_x = 179210853392303317793440285562762725654
# g_y = 105268671499942631758568591033409611165
# G = E(g_x, g_y)
#
#
# # Bob's public key
# b_x = 272640099140026426377756188075937988094
# b_y = 51062462309521034358726608268084433317
# Qb = E(b_x,b_y)
#
# # Lets find bobs private key
# dB = G.discrete_log(Qb)
# print(dB)
# 23364484702955482300431942169743298535


our_private_key = Point(
    x=280810182131414898730378982766101210916, y=291506490768054478159835604632710368904
)

dB = 23364484702955482300431942169743298535

shared_secret = double_and_add(our_private_key, dB)
print(shared_secret.x)
