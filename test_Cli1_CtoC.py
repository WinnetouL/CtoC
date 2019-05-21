# to client-2: receive msg; send msg; receive msg
# within defined functions
# just one socket in use
# modular structure

import socket
import time
import sys



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


    def main(self):
        print("---- Client 1 active ----")
 ###### NEW ######
        a = self.sock.getsockname()
        print('Connection from: client-1qqqqqqqqqqqqqqqq ', a[0], 'to CLIENT-2222222222222: ', self.addr[0])      # instead of "self.addr" I could just use TCP_IP
        self.receiveCli1()
        self.sendCli1()
 ###### NEW ###### 
        try:
            self.receiveCli1()
        except ConnectionResetError as e:
            print("TROLLLLLLLLLLLLLLLLL", e)
            time.sleep(3)
            print("return to main")
            self.__init__()
            self.main()
    

    def receiveCli1(self):

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


    def sendCli1(self):

        while True:
            msg = "Welcome from CLIENT-1!"
            msg = f"{len(msg):<{client1Class.HEADERSIZE}}" + msg
            self.conn.send(bytes(msg, "utf-8"))
            break



client1Object = client1Class()
client1Object.main()




# self.conn.close()???
