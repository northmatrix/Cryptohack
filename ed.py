from typing import Tuple, Dict
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from sympy.ntheory import sqrt_mod

sha1_hash = hashlib.sha1()


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


# Ths is only the x coordinate of point Q from user a so lets find Qy and complete Q
def curve_to_point_p3mod4(px: int, E: dict[str, int]) -> Tuple[int, int]:
    y2 = pow(px, 3, E["C"]) + (E["A"] * px) + E["B"]
    y2 %= E["C"]
    # now since p is of form = 3 mod 4 then we can use equation to get root y
    y = pow(y2, (E["C"] + 1) // 4, E["C"])
    return (px, y)


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


# Cryptohack challenge 1
E = {"A": 497, "B": 1768, "C": 9739}
p = (493, 5564)
q = (1539, 4742)
r = (4403, 5202)
p1 = ed_add(p, p, E)
p2 = ed_add(q, r, E)
s = ed_add(p1, p2, E)
print("Challenge 1:  ", s)


# Cryptohack challenge 2
x = (5323, 5438)
s = ed_scalar(x, 1337, E)
p = (2339, 2213)
q = ed_scalar(p, 7863, E)
print("Challenge 2:  ", q)

# Cryptohack challenge 3
E = {"A": 497, "B": 1768, "C": 9739}
q = (815, 3190)
nb = 1829
secret = ed_scalar(q, nb, E)
sha1_hash.update(str(secret[0]).encode())
print("Challenge 3:  ", sha1_hash.hexdigest())

# Cryptohack challenge 4
G = (1804, 5368)
E = {"A": 497, "B": 1768, "C": 9739}
xQa = 4726
xyQa = curve_to_point_p3mod4(xQa, E)
nb = 6534
shared_secret = ed_scalar(xyQa, nb, E)
iv = "cd9da9f1c60925922377ea952afc212c"
ciphertext = "febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8"
print("Challenge 4:  ", decrypt_flag(shared_secret[0], iv, ciphertext))


# Cryptohack challenge 5
# Montgomery binary algorithm in group
# Addition formula
def ed_affine_add(
    p: Tuple[int, int], q: Tuple[int, int], E: Dict[str, int]
) -> Tuple[int, int]:
    (x1, y1), (x2, y2) = p, q
    a = (y2 - y1) * pow(x2 - x1, -1, E["C"])
    x3 = (E["B"] * pow(a, 2)) - E["A"] - x1 - x2
    y3 = a * (x1 - x3) - y1
    return (x3 % E["C"], y3 % E["C"])


# Double formula
def ed_affine_double(p: Tuple[int, int], E: Dict[str, int]) -> Tuple[int, int]:
    (x1, y1) = p
    a = (3 * pow(x1, 2, E["C"]) + 2 * E["A"] * x1 + 1) * pow(
        2 * E["B"] * y1, -1, E["C"]
    )
    x3 = E["B"] * pow(a, 2, E["C"]) - E["A"] - 2 * x1
    y3 = a * (x1 - x3) - y1
    return (x3 % E["C"], y3 % E["C"])


# Montgomery binary algorithm
def montgomery_bin_algorithm(
    p: Tuple[int, int], k: int, E: dict[str, int]
) -> Tuple[int, int]:
    R0 = p
    R1 = ed_affine_double(p, E)
    for i in bin(k)[3:]:
        if i == "0":
            (R0, R1) = (ed_affine_double(R0, E), ed_affine_add(R0, R1, E))
        else:
            (R0, R1) = (ed_affine_add(R0, R1, E), ed_affine_double(R1, E))
    return R0


E = {"B": 1, "A": 486662, "C": pow(2, 255) - 19}


def curve_x_to_point(qx, E):
    y2 = (pow(qx, 3, E["C"]) + E["A"] * pow(qx, 2, E["C"]) + qx) * pow(
        E["B"], -1, E["C"]
    )
    y2 = y2 % E["C"]
    y = sqrt_mod(y2, E["C"])
    return (qx, y)


gx = 9
# so i know that g is correct
g = curve_x_to_point(gx, E)
print("G is: ", g)
s = montgomery_bin_algorithm(g, 0x1337C0DECAFE, E)
print(s)


# Cryptohack challenge 6
