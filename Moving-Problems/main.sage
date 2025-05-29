# sage
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from sage.all import GF, EllipticCurve, ZZ, gcd


def decrypt_flag(shared_secret):
    iv = bytes.fromhex("eac58c26203c04f68d63dc2c58d79aca")
    ct = bytes.fromhex(
        "bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d"
    )

    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    pt = unpad(cipher.decrypt(ct), 16)
    return pt


p = 1331169830894825846283645180581
a = -35
b = 98

E = EllipticCurve(GF(p), [a, b])
G = E((479691812266187139164535778017, 568535594075310466177352868412))
Alice = E((1110072782478160369250829345256, 800079550745409318906383650948))
Bob = E((1290982289093010194550717223760, 762857612860564354370535420319))

order = G.order()
k = 1
while (p**k - 1) % order:
    k += 1

Ee = EllipticCurve(GF(p ^ k, "y"), [a, b])
Ge = Ee(G)
Ae = Ee(Alice)

T = Ee.random_point()
M = T.order()
d = gcd(M, G.order())
Q = (M // d) * T

assert G.order() / Q.order() in ZZ

N = G.order()

a = Ge.weil_pairing(Q, N)
b = Ae.weil_pairing(Q, N)

na = b.log(a)
assert na * G == Alice

priv_key = (na * Bob).xy()[0]

print(decrypt_flag(priv_key))
