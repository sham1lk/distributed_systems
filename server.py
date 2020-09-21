from threading import Thread
import socket
import operator
import tqdm
import os
from functools import reduce


class ClientListener(Thread):
    def __init__(self, sock, addr):
        super().__init__(daemon=True)
        self.sock = sock
        self.addr = addr

    def run(self):
        try:
            filename = self.sock.recv(4098).decode()
            filename = os.path.basename(filename)
            filename = self._edit_name(filename)

            file_path = "./{}".format(filename)

            with open(file_path, "wb") as f:
                while (True):
                    bytes_read = self.sock.recv(4098)
                    if not bytes_read:
                        break
                    f.write(bytes_read)

                print("[+] File received: {}".format(filename))
            self.sock.close()
            print("Disconnected.")
        except:
            print("Something went wrong contact your system administrator")

    def _edit_name(self, filename):
        after_dot = filename.split(".")
        head = after_dot[0]
        tail = ".".join(after_dot[1:])
        n = 0
        while os.path.isfile("./{}".format(filename)):
            n += 1
            if len(after_dot) == 1:
                filename = "{}_copy{}".format(head, n)
            else:
                filename = "{}_copy{}.{}".format(head, n, tail)

        return filename


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 5050))
    print("Server created.")
    s.listen()
    while True:
        con, addr = s.accept()
        print("Connected.")
        ClientListener(con, addr).start()


if __name__ == "__main__":
    main()
