# to client 1: send messages
# within defined functions

import socket



class client2Class:
    
    HEADERSIZE = 10
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 1234


    def __init__(self):    
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((client2Class.IP, client2Class.PORT))
        # print(socket.gethostbyname(socket.gethostname()))  - print out current IP
        self.sock.listen(3)
        # sock.close shutdown


    def main(self):
        print("---Client 1 active---")
        while True:
            # double assignement of the return values from the accept function
            conn, address = self.sock.accept()
            print(f"Connection from {address} has been established!")
            msg = "Welcome from client 1!"
            msg = f"{len(msg):<{client2Class.HEADERSIZE}}" + msg
            
            conn.send(bytes(msg, "utf-8"))

            while True:
                msg = input("send another msg to client 2: ")
                msg = f"{len(msg):<{client2Class.HEADERSIZE}}" + msg
                conn.send(bytes(msg, "utf-8"))

  
client2Object = client2Class()
client2Object.main()
