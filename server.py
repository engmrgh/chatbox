import asyncio

groups = {}

async def handle_echo(reader, writer):
    while True:
        # Read one line, where “line” is a sequence of bytes ending with \n.
        data = await reader.readline()
        try:
            message = data.decode()  # Return a string decoded from the given bytes.
        except:
            writer.close()
            return
        # socket:
        # 'peername': the remote address to which the socket is connected,
        # result of socket.socket.getpeername() (None on error)
        addr = writer.get_extra_info('peername')
        # {..!r} Calls repr() on the argument first
        print(f"Received {message!r} from {addr!r}")

        scommand = message.split(':')
        if len(scommand) == 1:
            command = scommand
        elif command == "quit":
            writer.close()
        else:
            writer.close()
            return

async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Bye Bye')


        loop.close()