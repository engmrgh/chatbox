import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8888         # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    socket_is_ok = True  # The socket is okay and running

    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Err 504. Server is not responding.")
        socket_is_ok = False

    while socket_is_ok:
        while socket_is_ok:
            data = input('> ')
            data += '\n'
            try:
                s.sendall(data.encode())
            except BrokenPipeError:
                print("Err 504. Server is not responding. Can't send message.")
                socket_is_ok = False
            if data == 'end':
                break

        while socket_is_ok:
            data = s.recv(1024)
            print(data.decode())
            if data.decode() == 'end':
                break
