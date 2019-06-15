# from client 1: receive messages
# within defined functions

import socket



class client1Class:

    HEADERSIZE = 10
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 1234


    def __init__(self):    
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((client1Class.IP, client1Class.PORT))
        

    def main(self):
        while True:
            fullMsg = ''
            newMsg = True

            while True:
                msg = self.sock.recv(16)
                
                if newMsg == True:
                    # printing out the first 10 characters (Headersize) of the message
                    print(f"first 10 characters of message: {msg[:client1Class.HEADERSIZE]}")
                    # append everything of the first 10 characters (Headersize) to 'msgLen'
                    # in our case it is always just the number of the length and blanks nothing else
                    # e.g.: 22
                    msgLen = int(msg[:client1Class.HEADERSIZE])
                    newMsg = False    
                    
                # appending 16 characters of the message per round of while loop to 'fullMsg'
                fullMsg += msg.decode("utf-8")
               # print(fullMsg)
                # checking if the (length of 'fullMsg' (1.round=16, 2.round=32)) - ('Headersize' (10 characters)) equals ('msgLen' (22))
                if len(fullMsg)-client1Class.HEADERSIZE == msgLen:
                    # if this is true full message is received. Printing everything out continuing after the 10 characters (Headersize)
                    print("----Full message recvd:----")
                    print(fullMsg[client1Class.HEADERSIZE:])
                    # in order to be able to get a next message we need to set 'newMsg' to true 
                    newMsg = True
                    fullMsg = ''


client1Object = client1Class()
client1Object.main()
