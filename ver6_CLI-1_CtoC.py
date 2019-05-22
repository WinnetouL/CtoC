# to client-2: receive msg; send msg; receive msg
# within defined functions
# just one socket in use
# modular structure
# prevent application from crashing due an expected 'ConnectionResetError' (connection handling) and restarting
# some tweaking for the userside

import socket
import asyncio


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
      


    async def main(self):

        try:
            print('Connection from: client-1 ', socket.gethostbyname(socket.gethostname()), ' to CLIENT-2: ', self.addr[0])      # instead of "self.addr" I could just use TCP_IP
            await self.receiveCli1()
            await self.sendCli1()
            # await self.receiveCli1()
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


    def mainTest(self): # ship into __init__()?
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.main())
        # loop.run_forever()
        loop.run_until_complete(self.main())
        loop.close()


client1Object = client1Class()
client1Object.mainTest() # seems like it is not needed if mainTest() gets shipped into __init__()

























'''
import asyncio


class how:

    def __init__(self):
        print("BOOOOM")

    async def snmp(self):
        print("Doing the snmp thing")
        await asyncio.sleep(1)

    async def proxy(self):
        print("Doing the proxy thing")
        await asyncio.sleep(2)

    async def main(self):
        while True:
            await self.snmp()
            await self.proxy()

    def crazt(self):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.main()) # However if you need to create task from arbitrary awaitable, you should use asyncio.ensure_future(obj) vs. loop.create_task(self.main())
        loop.run_forever()


howOb = how()
howOb.crazt()
'''