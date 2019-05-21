# to client 1: receive msg; send msg; receive msg
# within defined functions

import socket




class client2Class:
    # class variabels: 
    HEADERSIZE = 10
    IP = socket.gethostbyname(socket.gethostname())     # IP ~ "192.168.2.111"
    PORT = 1234
    PORT2 = 1235

    # connect to the default port
    def __init__(self):    
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock1.connect((client2Class.IP, client2Class.PORT))      # connect to client 1 socket


    def main(self):
        print("---- Client 2 active ----")
        
        while True:
            fullClient1Msg = ''
            newClient1Msg = True

            while True:
                msg = self.sock1.recv(16)
                
                if newClient1Msg == True:        # the if part will be passed just once to figure out how long the msg will be, because newClientRespond is going to be set to false
                    print(f"first 10 characters of message: {msg[:client2Class.HEADERSIZE]}")        # printing out the first 10 characters (Headersize) of the message
                    msgLen = int(msg[:client2Class.HEADERSIZE])      # append everything of the first 10 characters (Headersize) to 'msgLen'. In our case it is always just the number of the length and blanks nothing else, so e.g.: 22
                    newClient1Msg = False    
                    
                fullClient1Msg += msg.decode("utf-8")        # decode the chunks of the received msg by given transformation format and append 16 characters each turn of the while loop to the full msg variable ('fullClient1Msg')
                
                if len(fullClient1Msg)-client2Class.HEADERSIZE == msgLen:     # this part is only going to be passed if the (length of 'fullClient1Msg' (1.round=16, 2.round=32 (next 16 'or less'))) - ('Headersize' (10 characters)) equals the determined ('msgLen' (22))
                    print("----Full message recv:----")
                    print(fullClient1Msg[client2Class.HEADERSIZE:])       # if this is true full message is received. Printing everything out continuing after the 10 characters (Headersize)
            
                    self.client2Send()
                    self.recvSecondMsg()



    def client2Send(self):
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.bind((client2Class.IP, client2Class.PORT2))
        sock2.listen(1)
        
        conn, address = sock2.accept()
        print(f"CLIENT 1 CONNECTED: {address} has been established!")
        respond = "Msg received! UFFFFFF"
        respond = f"{len(respond):<{client2Class.HEADERSIZE}}" + respond
        conn.send(bytes(respond, "utf-8"))



    def recvSecondMsg(self):
        fullClient1Msg2 = ''
        newClient1Msg2 = True
        
        while True:
            msg2 = self.sock1.recv(16)
            
            if newClient1Msg2 == True:
                print(f"first 10 characters of message UFFFFFF: {msg2[:client2Class.HEADERSIZE]}")
                msgLen2 = int(msg2[:client2Class.HEADERSIZE])
                newClient1Msg2 = False

            fullClient1Msg2 += msg2.decode("utf-8")
            
            if len(fullClient1Msg2)-client2Class.HEADERSIZE == msgLen2:
                print("----Full message recv:----")
                print(fullClient1Msg2[client2Class.HEADERSIZE:])
                newClient1Msg2 = True        # in order to be able to get a next message we need to set 'newClient1Msg' to true
                fullClient1Msg2 = ''         # and reset 'fullClient1Msg2'



client2Object = client2Class()
client2Object.main()







'''
import socket


class client2Class:
    TCP_IP = socket.gethostbyname(socket.gethostname()) 
    TCP_PORT = 1234
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response


    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((client2Class.TCP_IP, client2Class.TCP_PORT))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()


    def Rrecv(self):
        print('Connection address:', self.addr)
        
        while True:
            data = self.conn.recv(client2Class.BUFFER_SIZE)
            
            if not data:
                break
            
            print("received data:", data.decode("utf-8"))
            print("done")
            break
            

    def sendMsg(self):
        print("hier sind wir")
        data2 = "dsadas"
        self.conn.send(bytes(data2, "utf-8"))  


    def main(self):
        print("---- Client active ----")
        
        self.Rrecv()
        self.sendMsg()
        #self.conn.close()




client2Object = client2Class()
client2Object.main()
'''