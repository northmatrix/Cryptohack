from typing import Tuple, Dict
import hashlib

sha1_hash = hashlib.sha1()


def ed_add(
    p: Tuple[int, int], q: Tuple[int, int], E: Dict[str, int]
) -> Tuple[int, int]:
    if p == (0, 0):
        return q
    elif q == (0, 0):
        return p
    if (p[0] == q[0]) and (p[1] == -q[1]):
        return (0, 0)
    else:
        la: int = 0
        if p != q:
            la: int = (q[1] - p[1]) * pow((q[0] - p[0]) % E["C"], -1, E["C"])
        if p == q:
            la: int = (3 * pow(p[0], 2, E["C"]) + E["A"]) * pow(2 * p[1], -1, E["C"])
        x3: int = (pow(la, 2, E["C"]) - p[0] - q[0]) % E["C"]
        y3: int = (la * (p[0] - x3) - p[1]) % E["C"]
        return (x3, y3)


def ed_scalar(p: Tuple[int, int], n: int, E: Dict[str, int]) -> Tuple[int, int]:
    q: Tuple[int, int] = p
    r: Tuple[int, int] = (0, 0)
    while n > 0:
        if n % 2 == 1:
            r = ed_add(r, q, E)
        q = ed_add(q, q, E)
        n = n // 2
    return (r[0] % E["C"], r[1] % E["C"])


E = {"A": 497, "B": 1768, "C": 9739}
p = (493, 5564)
q = (1539, 4742)
r = (4403, 5202)
p1 = ed_add(p, p, E)
p2 = ed_add(q, r, E)
s = ed_add(p1, p2, E)
print(s)

x = (5323, 5438)
s = ed_scalar(x, 1337, E)
print(s)
p = (2339, 2213)
q = ed_scalar(p, 7863, E)
print(q)

# Cryptohack challenge 3
E = {"A": 497, "B": 1768, "C": 9739}
q = (815, 3190)
nb = 1829
secret = ed_scalar(q, nb, E)
sha1_hash.update(str(secret[0]).encode())
print(sha1_hash.hexdigest())

# Cryptohack challenge 4
E = {"A": 497, "B": 1768, "C": 9739}
G = (1804, 5368)
xQa = 4726
nb = 6534
xQb = ed_scalar(G, nb, E)
shared_secret = ed_scalar(xQb, xQa, E)

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1] :]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode())
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext_b = bytes.fromhex(ciphertext)
    iv_b = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv_b)
    plaintext = cipher.decrypt(ciphertext_b)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode()
    else:
        return plaintext.decode()


iv = "cd9da9f1c60925922377ea952afc212c"
ciphertext = "febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8"

print(decrypt_flag(shared_secret[0], iv, ciphertext))
