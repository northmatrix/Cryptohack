import socket
import json
from datetime import datetime
import hashlib
import time
from ecdsa.ecdsa import generator_192
from Crypto.Util.number import bytes_to_long, long_to_bytes
from ecdsa.ecdsa import Public_key, Private_key, Signature

# Setup cryptographic components
g = generator_192
n = g.order()
k = 1


def sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    return sha1_hash.digest()


# Setup socket
s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.connect(("socket.cryptohack.org", 13381))

try:
    # First request - get the signed time
    data = {"option": "sign_time"}
    json_data = json.dumps(data)

    while True:
        now = datetime.now()
        seconds_past = int(now.strftime("%S"))

        # Only proceed when seconds is 2
        if seconds_past == 2:
            try:
                # Send initial request
                s_socket.send(json_data.encode())
                response = s_socket.recv(1024).decode("utf-8").strip()
                print(f"First response: {response}")

                # Process the response
                try:
                    json_obj = json.loads(response)
                    s = int(json_obj["s"], 16)
                    r = int(json_obj["r"], 16)
                    z = bytes_to_long(sha1(json_obj["msg"].encode()))

                    # Calculate private key
                    dA = (((s * k - z) % n) * pow(r, -1, n)) % n

                    # Create verification request
                    temp = {
                        "option": "verify",
                        "msg": "unlock",
                        "r": "0x00",
                        "s": "0x00",
                    }

                    # Generate signature
                    pubkey = Public_key(g, g * dA)
                    privkey = Private_key(pubkey, dA)
                    z = bytes_to_long(sha1(b"unlock"))
                    sig = privkey.sign(z, 1)

                    # Format signature values
                    temp["r"] = hex(sig.r)
                    temp["s"] = hex(sig.s)

                    # Send verification request
                    fake_str = json.dumps(temp)
                    print(f"Sending verification: {fake_str}")
                    s_socket.send(fake_str.encode())

                    # Get final response
                    final_response = s_socket.recv(1024).decode("utf-8").strip()
                    print(f"Final response: {final_response}")

                    # Try to parse final response as JSON if possible
                    try:
                        final_json = json.loads(final_response)
                        print("Parsed final response:", final_json)
                    except json.JSONDecodeError:
                        # It's okay if the final response isn't JSON
                        pass

                    print("END")
                    break  # Exit after successful attempt

                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                except Exception as e:
                    print(f"Error processing response: {e}")

            except socket.error as e:
                print(f"Socket error: {e}")

        # Small delay to avoid high CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting program...")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    s_socket.close()
    print("Socket closed")
