import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad  # , unpad
import os

# This is the flag and it is what we want to retrive
FLAG = b"crypto{??????????????????????????????????????}"


# Generate shared secret
def gen_keypair(G, p):
    # we select a randim int range 1 - (p - 1)
    n = random.randint(1, (p - 1))
    # sclar mult with generator point to create a public key
    P = n * G
    # return the private key (n) and the public key (P)
    return n, P


def gen_shared_secret(P, n):
    # This takes your private key and senders public key and generates shared secret x coordinate
    S = P * n
    return S.xy()[0]


# This is standard 128-Bit AES CBC mode encrypting flag with shared secret as key
def encrypt_flag(shared_secret: int):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]
    # Encrypt flag
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    # Prepare data to send
    data = {}
    data["iv"] = iv.hex()
    data["encrypted_flag"] = ciphertext.hex()
    return data


# Define Curve params
# Weistrsass curve
p = 1331169830894825846283645180581
a = -35
b = 98
E = EllipticCurve(GF(p), [a, b])
G = E.gens()[0]

# Generate 2  keypairs
n_a, P1 = gen_keypair(G, p)
n_b, P2 = gen_keypair(G, p)

# Calculate shared secret
S1 = gen_shared_secret(P1, n_b)
S2 = gen_shared_secret(P2, n_a)

# Check protocol works ( This should work)
assert S1 == S2

# Now we encrypt the flag with our shared secret
flag = encrypt_flag(S1)

# This the output to analyse
print(f"Generator: {G}")
print(f"Alice Public key: {P1}")
print(f"Bob Public key: {P2}")
print(f"Encrypted flag: {flag}")
