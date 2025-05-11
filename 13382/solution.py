# Define the curve parameters
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B


# Define the elliptic curve over the finite field GF(p)
E = EllipticCurve(GF(p), [a, b])


# Define the public key params
x = 0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531
y = 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A
P = E(x, y)


G = E(
    0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
)
print("Public Key: ", P)
print("Generator Point: ", G)


# Let n be some scalar value
n = 2
invn = pow(n, -1, E.order())  # Compute the modular inverse of n

# Calculate G from P as invn * P
G_Calculated = invn * P
print(G_Calculated)
# Now calculate P = n * G_Calculated to verify the relationship
PUBLIC = n * G_Calculated
print("Public Key (after calculation): ", PUBLIC)
