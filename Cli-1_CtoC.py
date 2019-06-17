# to client 2: send messages

import socket



HEADERSIZE = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 1234))
sock.listen(3)


while True:
    # double assignement of the return values from the accept function
    clientsocket, address = sock.accept()
    print(f"Connection from {address} has been established!")
    
    msg = "Welcome from client 1!"
    # msg = input("send msg to client: ")
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    
    clientsocket.send(bytes(msg, "utf-8"))
   
    while True:
        msg = input("send another msg to client 1: ")
        msg = f"{len(msg):<{HEADERSIZE}}" + msg
        clientsocket.send(bytes(msg, "utf-8"))
        # msg = "Welcome from client 1!"




# print(msg, "dsadsfdf")
# sending a message which includes the length of the message and
# putting 10 characters (Headersize) in front (includes the length of the message)
# e.g.: 22        Welcome from client 1! dsadsfdf
# run into problems when the message length has more then 10 digits
