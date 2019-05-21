# to client 2: send msg; receive msg; send msg
# within defined functions

import socket



class client1Class:
    # class variabels: 
    HEADERSIZE = 10
    IP = socket.gethostbyname(socket.gethostname())     # IP ~ "192.168.2.111"
    PORT = 1234
    PORT2 = 1235

    # initalize default used port
    def __init__(self):    
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # SOCK_STREAM -> TCP
        self.sock1.bind((client1Class.IP, client1Class.PORT))
        self.sock1.listen(1)


    def main(self):
        print("---- Client 1 active ----")
        
        while True:
            conn, address = self.sock1.accept()      # the accept funtion returns 2 values, which get assigned to variable
            print(f"CLIENT 2 CONNECTED: {address} has been established!")
            msg = "Welcome from client 1!"
            msg = f"{len(msg):<{client1Class.HEADERSIZE}}" + msg     # rebuild msg: counting length of msg and append the length number in front of the msg within the defined headersize
            conn.send(bytes(msg, "utf-8"))      # send msg in given transformation format      
            self.client1Recv()

            while True:     # calling sendSecondMsg() function over and over again
                msg1 = input("send another msg to client 2: ")
                self.sendSecondMsg(conn, msg1)


    def client1Recv(self):
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect((client1Class.IP, client1Class.PORT2))     	# connect to client socket
        
        while True:
            fullClient2Respond = ''
            newClient2Respond = True

            while True:
                chunkClient2Respond = sock2.recv(16)

                if newClient2Respond == True:        
                    print(f"first 10 characters of message: {chunkClient2Respond[:client1Class.HEADERSIZE]}")
                    respondLen = int(chunkClient2Respond[:client1Class.HEADERSIZE])
                    newClient2Respond = False 

                fullClient2Respond += chunkClient2Respond.decode("utf-8")

                if len(fullClient2Respond)-client1Class.HEADERSIZE == respondLen:
                    print("----Full message recv:----")
                    print("from Client 2: " + fullClient2Respond[client1Class.HEADERSIZE:])
                    break
            break
             

    def sendSecondMsg(self, conn, msg1):
        print("Going to be send: ", msg1)
        msg1 = f"{len(msg1):<{client1Class.HEADERSIZE}}" + msg1
        conn.send(bytes(msg1, "utf-8"))


  
client1Object = client1Class()
client1Object.main()




# keep in mind:
# self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock.close shutdown
# sock2.setblocking(True)











'''
import socket
 

class client1Class:
    TCP_IP = socket.gethostbyname(socket.gethostname()) 
    TCP_PORT = 1234
    BUFFER_SIZE = 1024
    MESSAGE = "Hello, World!"


    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((client1Class.TCP_IP, client1Class.TCP_PORT))
        

    def send(self):
        self.s.send(bytes(client1Class.MESSAGE, "utf-8"))


    def recvSecondMsg(self):
        data = self.s.recv(client1Class.BUFFER_SIZE)
        self.s.close()
        print("received data:", data.decode("utf-8"))


    def main(self):
        print("---- Server active ----")

        self.send()
        self.recvSecondMsg()



client1Object = client1Class()
client1Object.main()
'''