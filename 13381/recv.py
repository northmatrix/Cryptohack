import socket
import json
from datetime import date, datetime
import hashlib
from ecdsa.ecdsa import generator_192
from Crypto.Util.number import bytes_to_long, long_to_bytes
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192

g = generator_192
n = g.order()
k = 1


def sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    return sha1_hash.digest()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("socket.cryptohack.org", 13381))
print(server.recv(4096))
data = {"option": "sign_time"}
json_data = json.dumps(data)

while True:
    now = datetime.now()
    if int(now.strftime("%S")) == 2:
        server.send(json_data.encode())
        response = server.recv(4096).decode("utf-8").strip()
        try:
            json_response = json.loads(response)
            s = int(json_response["s"], 16)
            r = int(json_response["r"], 16)
            z = bytes_to_long(sha1(json_response["msg"].encode()))

            dA = (((s * k - z) % n) * pow(r, -1, n)) % n
            temp = {"option": "verify", "msg": "unlock", "r": "0x00", "s": "0x00"}
            pubkey = Public_key(g, g * dA)
            privkey = Private_key(pubkey, dA)

            z = bytes_to_long(sha1(b"unlock"))
            sig = privkey.sign(z, 1)
            temp["r"] = str(hex(sig.r))
            temp["s"] = str(hex(sig.s))
            fake_str = json.dumps(temp)

            server.send(fake_str.encode())
            result = server.recv(4096).decode("utf-8").strip()
            print(result)
            break
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
