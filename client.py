# + set username
# + provide functionality to switch contact to chat with, quit and send messages

import socket
import threading


class clientClass:
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 10
    USERNAME = ""

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((clientClass.TCP_IP, clientClass.TCP_PORT))
        print("---- Client active ----\n")

    def main(self):
        print("Connection from client: ", socket.gethostbyname(socket.gethostname()), " to server: ", clientClass.TCP_IP, "\n")
        t0 = threading.Thread(target=self.send, args=("!!!!",))
        t0.start()
        t1 = threading.Thread(target=self.recv)
        t1.daemon = True
        t1.start()
        typeOfMsgList = ["{switch}", "{quit}"]
        while True:
            rawInput = input(f"<{clientClass.USERNAME}> ({{switch}}/{{quit}})")
            if rawInput not in typeOfMsgList:
                t2 = threading.Thread(target=self.send, args=(rawInput,))
                t2.start()
            else:
                t2 = threading.Thread(target=self.send, args=(rawInput,))
                t2.start()

    def send(self, msgOrTypeOfMsg="!"):
        if msgOrTypeOfMsg == "{switch}":
            print(msgOrTypeOfMsg, "switch")
        elif msgOrTypeOfMsg == "{quit}":
            print(msgOrTypeOfMsg, "quit")
        elif msgOrTypeOfMsg == "!!!!":
            clientClass.USERNAME = input("Username ? ")
            print(f"--> You chose {clientClass.USERNAME}\n")
            userNamePrefix = msgOrTypeOfMsg + str(len(clientClass.USERNAME))
            msg = f"{userNamePrefix:<{clientClass.HEADERSIZE}}" + clientClass.USERNAME
            self.sock.send(bytes(msg, "utf-8"))
        else:
            msg = ""
            msg = f"{len(msgOrTypeOfMsg):<{clientClass.HEADERSIZE}}" + msgOrTypeOfMsg
            self.sock.send(bytes(msg, "utf-8"))

    def recv(self):
        try:
            while True:
                fullServerMsg = ""
                newServerMsg = True
                while True:
                    msg = self.sock.recv(16)
                    if newServerMsg is True:
                        msgLen = int(msg[: clientClass.HEADERSIZE])
                        newServerMsg = False
                    fullServerMsg += msg.decode("utf-8")
                    if len(fullServerMsg) - clientClass.HEADERSIZE == msgLen:
                        print("\n<server> ", fullServerMsg[clientClass.HEADERSIZE :])
                        break
        except ConnectionResetError as e:
            print("Server closed the connection\n", "OS-Error:", e, "\nApplication quitted")


clientObject = clientClass()
clientObject.main()
