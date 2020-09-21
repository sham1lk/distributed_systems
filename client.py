import socket
from tqdm import tqdm
import os
import sys

if len(sys.argv) != 4:
    print("incorrect command! usage: python3 client.py <file> <host> <port> "
          "pls try again!")
    sys.exit(1)

filename = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

s = socket.socket()
s.connect((host, port))
print("[+] Connected.")

filesize = os.path.getsize(filename)
s.send(filename.encode())

progress = tqdm(range(filesize), "[*] Sending {}".format(filename))

with open(filename, "rb") as f:
    for _ in progress:
        bytes = f.read(4098)
        if not bytes:
            break
        s.sendall(bytes)
        progress.update(len(bytes))

if bytes == filesize:
    print("[+] File was successfully sent.".format(filename))
else:
    print("[+] File was sent, but something went wrong.".format(filename))

s.close()
