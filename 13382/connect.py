import json
import socket

# Prepare the data to send
data = {
    "private_key": 5214,  # Ensure private_key is a string
    "host": "www.bing.com",
    "curve": "secp256r1",
    "generator": {
        "x": 10966474992011734935882366762732671727782719651294529032556338235210348910401,
        "y": 10966474992011734935882366762732671727782719651294529032556338235210348910401,
    },
}

# Convert the dictionary to a JSON string
json_data = json.dumps(data)

# Establish a socket connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect(("socket.cryptohack.org", 13382))
        s.sendall(json_data.encode("utf-8"))  # Send as UTF-8 encoded string

        # Receive data from the server (adjust the buffer size if necessary)
        response = s.recv(1024)

        if response:
            print("Response received:", response.decode("utf-8"))
        else:
            print("No response or connection was closed by the server.")

    except Exception as e:
        print(f"Error occurred: {e}")
