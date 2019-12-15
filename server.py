import asyncio

groups = dict()


async def join_group(gid, usr, writer):
    if gid in groups:
        groups[gid].append(usr)
    else:
        groups[gid] = []
        groups[gid].append(usr)
    message = f"You have been added to group with id {gid}"
    writer.write(message.encode())
    print(f"I have added usr {usr} to group with id {gid}")
    return


async def handle_echo(reader, writer):
    while True:
        # Read one line, where “line” is a sequence of bytes ending with \n.
        data = await reader.readline()
        if reader.at_eof():
            return
        if data.decode() == "end\n":
            return
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