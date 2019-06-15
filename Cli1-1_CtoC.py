# dynamic chatting
# within defined functions
# just one socket in use
# modular structure
# prevent application from crashing due an expected 'ConnectionResetError' (connection handling) and restarting

import sys
import time
import socket
import threading



class client1Class:
    # class variabels:
    TCP_IP = socket.gethostbyname(socket.gethostname())
#    TCP_IP = '192.168.2.134'
    TCP_PORT = 1234
    HEADERSIZE = 10

    # initalize socket
    def __init__(self):
        print("---- Client 1 active - waiting for connections ----\n")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # AF_INET = IPv4 | SOCK_STREAM = TCP
        self.sock.bind((client1Class.TCP_IP, client1Class.TCP_PORT))
        self.sock.listen(1)     # "number of unaccepted connections that the system will allow before refusing new connections"
        self.conn, self.addr = self.sock.accept()       # the accept funtion returns 2 values, which get assigned to variable
        

    def main(self):
        print('Connection from: client-1 ', socket.gethostbyname(socket.gethostname()), ' to CLIENT-2: ', self.addr[0])      # instead of "self.addr" I could just use TCP_IP
    
        t0 = threading.Thread(target = self.recvCli1)
        t1 = threading.Thread(target = self.sendCli1)
    
        while True:
            if t0.is_alive() == False:
                t0 = threading.Thread(target = self.recvCli1)
                t0.daemon = True        # mark these functiones as daemon threads, which are parts of the main thread (main > daemon).
                t0.start()  
            elif t1.is_alive() == False:
                t1 = threading.Thread(target = self.sendCli1)
                t1.daemon = True        # This enables the possibility to stop the main thread with cmd + c and the other threads will stop as well, because they are daemons. Otherwise the started threads would continuously run.
                t1.start()
            else:
                time.sleep(2)       # a = threading.active_count() | print("Threads alive: ", a)
                pass
                
        
    def recvCli1(self):
        try:
            while True:
                fullClient2Msg = ''
                newClient2Msg = True
                
                while True:
                    msg = self.conn.recv(16)        # 'print(self.conn)' to see that the raddr port changes
                    if newClient2Msg == True:        # the if part will be passed just once to figure out how long the msg will be, because newClientRespond is going to be set to false
                        print(f"First 10 characters of Client-2's message: {msg[:client1Class.HEADERSIZE]}")       # printing out the first 10 characters (Headersize) of the message
                        msgLen = int(msg[:client1Class.HEADERSIZE])      # append everything of the first 10 characters (Headersize) to 'msgLen'. In our case it is always just the number of the length and blanks nothing else, so e.g.: 22
                        newClient2Msg = False
                    
                    fullClient2Msg += msg.decode("utf-8")        # decode the chunks of the received msg by given transformation format and append 16 characters each turn of the while loop to the full msg variable ('fullClient2Msg')
                    
                    if len(fullClient2Msg)-client1Class.HEADERSIZE == msgLen:     # this part is only going to be passed if the (length of 'fullClient2Msg' (1.round=16, 2.round=32 (next 16 'or less'))) - ('Headersize' (10 characters)) equals the determined ('msgLen' (22))
                        print("Client-2's message received: ", fullClient2Msg[client1Class.HEADERSIZE:])        # if this is true full message is received. Printing everything out continuing after the 10 characters (Headersize)
                        break
        except ConnectionResetError as e1:
            print("Client-2 closed the window\n", "OS-Error:", e1, "\nApplication restarted")
            self.__init__()     # due interruption of the connection (ConnectionResetError "raised when a connection is reset by the peer"), I suppose I need to run my socket setup function again, which causes a port (raddr) change - just run main() again doesn't work.


    def sendCli1(self):
        while True:
            msg = input("Second msg to client-1?: ")
            msg = f"{len(msg):<{client1Class.HEADERSIZE}}" + msg
            self.conn.send(bytes(msg, "utf-8"))




client1Object = client1Class()
client1Object.main()
