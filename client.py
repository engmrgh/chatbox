import socket
import threading
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8888         # The port used by the server
socket_is_ok = True  # The socket is okay and running


def client_to_server(s: socket):
    global socket_is_ok
    data = "start"
    while data != "quit" and socket_is_ok:
        data = input('> ')
        data += '\n'
        try:
            s.sendall(data.encode())
        except BrokenPipeError:
            print("Err 504. Server is not responding. Can't send message.")
            socket_is_ok = False
            return


def server_to_client(s: socket):
    global socket_is_ok
    while socket_is_ok:
        data = s.recv(1024)
        data = data.decode()
        if data != "done":
            sys.stdout.write('\b')
            print("---", end='')
            print(data, end='')
            print("---<")
            sys.stdout.write("> ")
            sys.stdout.flush()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Err 504. Server is not responding.")
        socket_is_ok = False

    c2s = threading.Thread(target=server_to_client, args=(s,))
    s2c = threading.Thread(target=client_to_server, args=(s,))

    s2c.start()
    c2s.start()
    while(socket_is_ok):
        pass
