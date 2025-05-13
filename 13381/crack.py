import hashlib
from ecdsa.ecdsa import generator_192
from Crypto.Util.number import bytes_to_long, long_to_bytes

g = generator_192
bit_length = 192
N = g.order()


# k is only known at 2 seconds past the minute


def sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    return sha1_hash.digest()


data1 = {
    "msg": "Current time is 5:2",
    "r": "0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012",
    "s": "0x4ee1b0311d896516670e71c662d9eb7a506557074cdc1184",
}

data2 = {
    "msg": "Current time is 5:2",
    "r": "0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012",
    "s": "0x4ee1b0311d896516670e71c662d9eb7a506557074cdc1184",
}
# we knot that the public key private key and the random number
# k was the same used to sign these two keys so infact the key
# has leaked unintenntiaonly below we will extract it

msg1, r1, s1 = (
    data1["msg"],
    int(data1["r"], 16),
    int(data1["s"], 16),
)
msg2, r2, s2 = (
    data2["msg"],
    int(data2["r"], 16),
    int(data2["s"], 16),
)

z1 = bytes_to_long(sha1(msg1.encode()))
z2 = bytes_to_long(sha1(msg2.encode()))

# k = ((z1 - z2) * pow(s1 - s2, -1, N)) % N
k = 1

dA = ((s1 * k - z1) % N) * pow(r1, -1, N) % N

print("Private key: ", dA)

fake = {"option": "verify", "msg": "unlock", "r": "0xaa", "s": "0xaa"}

e = sha1("unlock".encode())
z = bytes_to_long(e)

x1, y1 = (k * g).x(), (k * g).y()
r = x1 % N
s = (pow(k, -1, N) * (z + r * dA)) % N

fake["r"] = str(hex(r))
fake["s"] = str(hex(s))
print(fake)
