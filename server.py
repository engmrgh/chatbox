import asyncio, socket
from datetime import datetime
from time import sleep

groups = dict()
connections = dict()


async def join_group(gid: int, usr, writer):  # TODO: user join group
    message = ""
    if gid in groups:
        if usr in groups[gid]:
            message = f"You are already a member of group {gid}"
        else:
            groups[gid].append(usr)
            message = f"You have been added to group with id {gid}"
    else:
        groups[gid] = []
        groups[gid].append(usr)
        message = f"Group {gid} has been created. And you have been added to the group"
    writer.write(message.encode())
    await writer.drain()
    print(f"I have added usr {usr} to group with id {gid}")
    print(groups)
    return


async def leave_group(gid: int, usr, writer):  # TODO: user left group
    message = ""
    deleted = False
    if gid in groups:
        if usr in groups[gid]:
            groups[gid].remove(usr)
            message = f"Successfully left the group {gid}"
            deleted = True
            if not groups[gid]:  # if group was empty destroy it
                del groups[gid]
                print(f"Group {gid} successfully destroyed")
        else:
            message = f"You are already out of group {gid}"
    else:
        message = f"Group with {gid} does not exist"
    writer.write(message.encode())
    await writer.drain()
    if deleted:
        print(f"I have removed usr {usr} from group with id {gid}")
    else:
        print(f"Request didn't change groups status")
    print(groups)
    return


async def send_group(gid: int, msg: str, writer, usr):
    message = ""
    added = False
    now = datetime.now()
    if gid in groups:
        for user in groups[gid]:
            w = connections[user][1]  # In the connections dictionary get the value of 3th index in which writer is in there
            if user == usr:
                continue
            msg = str(usr) + ":" + msg[:-1]
            w.write(msg.encode())
            await w.drain()
        message = f"Message successfully send"
    else:
        message = f"Group {gid} does not exist"
    writer.write(message.encode())
    await writer.drain()
    if added:
        print(f"I have added message {msg} to group with id {gid} on {now}")
    else:
        print(f"Message was not added to grp_msg")
    print(connections)
    return


async def quit_app(usr, writer):
    to_be_deleted = []
    for gid in groups:
        if usr in groups[gid]:
            to_be_deleted.append(gid)
    for val in to_be_deleted:
        await leave_group(val, usr, writer)
    writer.write("Your account has been deleted.".encode())
    print(f"I deleted user account {usr}")
    await writer.drain()
    del connections[usr]
    return


async def handle_echo(reader, writer):
    while True:
        # Read one line, where “line” is a sequence of bytes ending with \n.
        data = await reader.readline()
        if reader.at_eof():
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

        if addr not in connections:
            connections[addr] = (reader, writer)

        # {..!r} Calls repr() on the argument first
        print(f"Received {message!r} from {addr!r}")

        statement_length = len(message.split(' '))

        if statement_length == 1:

            if message.lower() == "quit\n".lower():
                await quit_app(usr=addr, writer=writer)
            elif message == '\n':
                err_message = "Type a statement please"
                err_message = err_message.encode()
                writer.write(err_message)
                await writer.drain()

        elif statement_length == 2:

            pmsg = message.split(' ')  # parted message
            if pmsg[0].lower() == "leave".lower():
                gid = int(pmsg[1])
                usr = addr
                await leave_group(gid=gid, usr=usr, writer=writer)
            elif pmsg[0].lower() == "join".lower():
                gid = int(pmsg[1])
                usr = addr
                await join_group(gid=gid, usr=usr, writer=writer)
            else:
                err_message = "Didn't understand statement " + message
                err_message = err_message.encode()
                writer.write(err_message)
                await writer.drain()

        elif statement_length >= 3:
            pmsg = message.split(' ')  # parted message
            if pmsg[0].lower() == "send".lower():
                gid = int(pmsg[1])
                msg = pmsg[2]
                await send_group(gid=gid, msg=msg, writer=writer, usr=addr)

        else:
            err_message = "Didn't understand statement" + message
            err_message = err_message.encode()
            writer.write(err_message)
            await writer.drain()
        sleep(0.2)  # This is just for having a nice look and feel
        writer.write("done".encode())
        await writer.drain()


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