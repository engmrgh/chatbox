import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1373         # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall('start'.encode())
    while True:
        while True:
            data = input('to send : ')
            s.sendall(data.encode())
            if data == 'end' :
                break
        while True:
            data = s.recv(1024)
            print(data.decode())
            if data.decode() == 'end':
                break
