import asyncio
import time



#class test:
 #   async def say_after(self, delay, what):
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

#async def main2(self):
async def main():
 
    print('crazy')

    task0 = asyncio.create_task(
        #self.say_after(1, 'hello'))
        say_after(1, 'hello'))

    task1 = asyncio.create_task(
        #self.say_after(2, 'world'))
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    
    await task0
    await task1


    print(f"finished at {time.strftime('%X')}")

    
asyncio.run(main())


#testobjec = test()
#testobjec.main(asyncio.run(main()))




'''
import asyncio


async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    message = input('new: ')
    print('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()



#message = 'Hello World!'
message = ''
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()







______________________________________________











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
    ssock, addr = lsock.accept()
    print(addr)
   # csock.setblocking(1) -> not needed?
    lsock.close()
    return (ssock)


async def wait_for_data():
    # Get a reference to the current event loop because
    # we want to access low-level APIs.
    loop = asyncio.get_running_loop()

    # Create a pair of connected sockets.
    rsock, wsock = socket.socketpair()
    sockets = pair()
    print('uff', sockets)

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