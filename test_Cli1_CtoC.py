import asyncio
import time
import socket







































'''
TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_PORT = 1234
HEADERSIZE = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)
conn, addr = sock.accept()
print(addr)       # the accept funtion returns 2 values, which get assigned to variable
print("---- Client 1 active - waiting for connections ----\n")
 

async def main():
    try:
        print('Connection from: client-1 ', socket.gethostbyname(socket.gethostname()), ' to CLIENT-2: ', addr[0])      # instead of "self.addr" I could just use TCP_IP
        
        task0 = asyncio.create_task(receiveCli1())
        task1 = asyncio.create_task(sendCli1())

        await task0
        await task1
        
    except ConnectionResetError as e:
        print("Client-2 closed the window\n", "OS-Error:", e, "\nApplication restarted")
        time.sleep(2)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((TCP_IP, TCP_PORT))
        sock.listen(1)
        print("---- Client 1 active - waiting for connections ----\n")
        main()
    conn, addr = sock.accept()       # the accept funtion returns 2 values, which get assigned to variable


async def receiveCli1():

    while True:
        fullClient2Msg = ''
        newClient2Msg = True

        while True:
            msg = conn.recv(16)

            if newClient2Msg == True:        # the if part will be passed just once to figure out how long the msg will be, because newClientRespond is going to be set to false
                print(f"First 10 characters of Client-2's message: {msg[:HEADERSIZE]}")       # printing out the first 10 characters (Headersize) of the message
                msgLen = int(msg[:HEADERSIZE])      # append everything of the first 10 characters (Headersize) to 'msgLen'. In our case it is always just the number of the length and blanks nothing else, so e.g.: 22
                newClient2Msg = False

            fullClient2Msg += msg.decode("utf-8")        # decode the chunks of the received msg by given transformation format and append 16 characters each turn of the while loop to the full msg variable ('fullClient2Msg')

            if len(fullClient2Msg)-HEADERSIZE == msgLen:     # this part is only going to be passed if the (length of 'fullClient2Msg' (1.round=16, 2.round=32 (next 16 'or less'))) - ('Headersize' (10 characters)) equals the determined ('msgLen' (22))
                print("Client-2's message received: ", fullClient2Msg[HEADERSIZE:])        # if this is true full message is received. Printing everything out continuing after the 10 characters (Headersize)
                break
        break


async def sendCli1():

    while True:
        msg = "Welcome from CLIENT-1!"
        msg = f"{len(msg):<{HEADERSIZE}}" + msg
        conn.send(bytes(msg, "utf-8"))
        break

while True:
    asyncio.run(main())



















    


class client1Class:
    # class variabels:
    TCP_IP = socket.gethostbyname(socket.gethostname())
#    TCP_IP = '192.168.2.134'
    TCP_PORT = 1234
    HEADERSIZE = 10

    # initalize default used port
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((client1Class.TCP_IP, client1Class.TCP_PORT))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()       # the accept funtion returns 2 values, which get assigned to variable
        print("---- Client 1 active - waiting for connections ----\n")
        asyncio.run(self.main())

    async def main(self):
        try:
            print('Connection from: client-1 ', socket.gethostbyname(socket.gethostname()), ' to CLIENT-2: ', self.addr[0])      # instead of "self.addr" I could just use TCP_IP
            
            task0 = asyncio.create_task(self.receiveCli1())
            task1 = asyncio.create_task(self.sendCli1())

            await task0
            await task1
            
        except ConnectionResetError as e:
            print("Client-2 closed the window\n", "OS-Error:", e, "\nApplication restarted")
            self.__init__()
            self.main()


    async def receiveCli1(self):

        while True:
            fullClient2Msg = ''
            newClient2Msg = True

            while True:
                msg = self.conn.recv(16)

                if newClient2Msg == True:        # the if part will be passed just once to figure out how long the msg will be, because newClientRespond is going to be set to false
                    print(f"First 10 characters of Client-2's message: {msg[:client1Class.HEADERSIZE]}")       # printing out the first 10 characters (Headersize) of the message
                    msgLen = int(msg[:client1Class.HEADERSIZE])      # append everything of the first 10 characters (Headersize) to 'msgLen'. In our case it is always just the number of the length and blanks nothing else, so e.g.: 22
                    newClient2Msg = False

                fullClient2Msg += msg.decode("utf-8")        # decode the chunks of the received msg by given transformation format and append 16 characters each turn of the while loop to the full msg variable ('fullClient2Msg')

                if len(fullClient2Msg)-client1Class.HEADERSIZE == msgLen:     # this part is only going to be passed if the (length of 'fullClient2Msg' (1.round=16, 2.round=32 (next 16 'or less'))) - ('Headersize' (10 characters)) equals the determined ('msgLen' (22))
                    print("Client-2's message received: ", fullClient2Msg[client1Class.HEADERSIZE:])        # if this is true full message is received. Printing everything out continuing after the 10 characters (Headersize)
                    break
            break


    async def sendCli1(self):

        while True:
            msg = "Welcome from CLIENT-1!"
            msg = f"{len(msg):<{client1Class.HEADERSIZE}}" + msg
            self.conn.send(bytes(msg, "utf-8"))
            break



client1Object = client1Class()
client1Object.main()
# asyncio.run(main())



'''




























'''
    async def say_after(delay, what):
        await asyncio.sleep(delay)
        print(what)

    async def main():
        task1 = asyncio.create_task(
            say_after(1, 'hello'))

        task2 = asyncio.create_task(
            say_after(2, 'world'))

        print(f"started at {time.strftime('%X')}")

        # Wait until both tasks are completed (should take
        # around 2 seconds.)
        await task1
        await task2

        print(f"finished at {time.strftime('%X')}")

    asyncio.run(main())







async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")














# https://asyncio.readthedocs.io/en/latest/tcp_echo.html
import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(writer.get_extra_info('sockname'))

    
    print("Received %r from %r" % (message, addr))

    # print("Send: %r" % message)
    new = input('newMsg ')
    print("Send: %r" % new)
 
    writer.write(bytes(new, 'utf-8'))
    await writer.drain()

    print("Close the client socket")
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
    
# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()












_________________________________________________________









import asyncio
import socket
import errno


def pair(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0):
    """Emulate the Unix socketpair() function on Windows."""
    # https://gist.github.com/geertj/4325783
    # We create a connected TCP socket. Note the trick with setblocking(0)
    # that prevents us from having to create a thread.
    lsock = socket.socket(family, type, proto)
    lsock.bind(('127.0.0.1', 1234)) 
    lsock.listen(1)
    #addr, port = lsock.getsockname()
    addr = '127.0.0.1'
    port = 1234
    csock = socket.socket(family, type, proto)
    csock.setblocking(0)
    try:
        csock.connect((addr, port))
    except socket.error as e:
        if e.errno != errno.WSAEWOULDBLOCK:
            raise
    csock.setblocking(0)
    lsock.close()
    
    print(csock)
    return (csock)


async def wait_for_data():
    # Get a reference to the current event loop because
    # we want to access low-level APIs.
    loop = asyncio.get_running_loop()

    # Create a pair of connected sockets.
    rsock, wsock = socket.socketpair()
    sockets = pair()
    print('tada', sockets)
    
    # Register the open socket to wait for data.
    reader, writer = await asyncio.open_connection(sock=rsock)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Wait for data
    data = await reader.read(100)

    # Got data, we are done: close the socket
    print("Received:", data.decode())
    writer.close()

    # Close the second socket
    wsock.close()

asyncio.run(wait_for_data())
'''




















'''
import asyncio
import socket
import errno


def pair(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0):
    """Emulate the Unix socketpair() function on Windows."""
    # https://gist.github.com/geertj/4325783
    # We create a connected TCP socket. Note the trick with setblocking(0)
    # that prevents us from having to create a thread.
    lsock = socket.socket(family, type, proto)
    lsock.bind(('127.0.0.1', 1234)) 
    lsock.listen(1)
    #addr, port = lsock.getsockname()
    addr = '127.0.0.1'
    port = 1234
    csock = socket.socket(family, type, proto)
   # csock.setblocking(0) -> not needed?
    csock.setblocking(0)
    try:
        csock.connect((addr, port))
    except socket.error as e:
        if e.errno != errno.WSAEWOULDBLOCK:
            raise
    ssock, addr = lsock.accept()
    print(ssock)
    print(addr)
   # csock.setblocking(1) -> not needed?
    csock.setblocking(1)
    lsock.close()
    print(ssock)
    print(csock)
    return (ssock, csock)


async def wait_for_data():
    # Get a reference to the current event loop because
    # we want to access low-level APIs.
    loop = asyncio.get_running_loop()

    # Create a pair of connected sockets.
    #rsock, wsock = socket.socketpair()
    sockets = pair()
    print(sockets[0])
    print(sockets[1])
    rsock = sockets[0]
    wsock = sockets[1]

    # Register the open socket to wait for data.
    reader, writer = await asyncio.open_connection(sock=rsock)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Wait for data
    data = await reader.read(100)

    # Got data, we are done: close the socket
    print("Received:", data.decode())
    writer.close()

    # Close the second socket
    wsock.close()

asyncio.run(wait_for_data())


'''
