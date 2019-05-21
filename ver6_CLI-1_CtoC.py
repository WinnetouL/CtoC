import asyncio
import socket


class MyProtocol(asyncio.Protocol):

    def __init__(self, loop):
        self.transport = None
        self.on_con_lost = loop.create_future()

    def connection_made(self, transport):
        self.transport = transport

    ######def data_received(self, data):
    #    print("Received:", data.decode())

        # We are done: close the transport;
        # connection_lost() will be called automatically.
      
        #self.transport.close()

    def connection_lost(self, exc):
        # The socket has been closed
        self.on_con_lost.set_result(True)


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # Create a pair of connected sockets
    wsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print(rsock)
    print(wsock)

    # Register the socket to wait for data.
    transport, protocol = await loop.create_connection(
        lambda: MyProtocol(loop), sock=wsock)
   
    print("useless var", transport)
    # Simulate the reception of data from the network.
    loop.call_soon(wsock.send, 'abc'.encode())

    try:
        await protocol.on_con_lost
    finally:
        print("FINALLY")
        #transport.close()
        #wsock.close()

asyncio.run(main())
























'''
import asyncio
import socket

async def wait_for_data():
    # Get a reference to the current event loop because
    # we want to access low-level APIs.
    loop = asyncio.get_running_loop()

    # Create a pair of connected sockets.
    rsock, wsock = socket.socketpair()

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