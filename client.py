# + set username
# + provide functionality to switch contact to chat with, quit and send messages

import time
import socket
import threading


class clientClass:
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 20
    USERNAME = ""
    LOCK = threading.Lock()

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((clientClass.TCP_IP, clientClass.TCP_PORT))
        print("---- Client active ----\n")

    def main(self):
        print("Connection from client: ", socket.gethostbyname(socket.gethostname()), " to server: ", clientClass.TCP_IP, "\n")
        t0 = threading.Thread(target=self.send, args=("{name}",))
        t0.start()
        t1 = threading.Thread(target=self.recv)
        t1.daemon = True
        t1.start()
        t2 = threading.Thread(target=self.send, args=("{switch}",))
        t2.start()
        while True:
            if t2.isAlive() is False:
                msgOrTypeOfMsg = input(f"<{clientClass.USERNAME}> ({{switch}}/{{quit}})")
                t3 = threading.Thread(target=self.send, args=(msgOrTypeOfMsg,))
                t3.start()
            else:
                time.sleep(2)
                pass

    def send(self, msgOrTypeOfMsg="!"):
        with clientClass.LOCK:
            if msgOrTypeOfMsg == "{switch}":
                switchPrefix = msgOrTypeOfMsg + str(len(msgOrTypeOfMsg))
                msg = f"{switchPrefix:<{clientClass.HEADERSIZE}}" + msgOrTypeOfMsg
                self.sock.send(bytes(msg, "utf-8"))
                destination = input("Send to?: ")
                switchPrefix = msgOrTypeOfMsg + str(len(destination))
                msg = f"{switchPrefix:<{clientClass.HEADERSIZE}}" + destination
                self.sock.send(bytes(msg, "utf-8"))
            elif msgOrTypeOfMsg == "{quit}":
                print(msgOrTypeOfMsg, "//quit")
            elif msgOrTypeOfMsg == "{name}":
                clientClass.USERNAME = input("Username ? ")
                print(f"--> You chose {clientClass.USERNAME}\n")
                userNamePrefix = msgOrTypeOfMsg + str(len(clientClass.USERNAME))
                msg = f"{userNamePrefix:<{clientClass.HEADERSIZE}}" + clientClass.USERNAME
                self.sock.send(bytes(msg, "utf-8"))
            else:
                msg = f"{len(msgOrTypeOfMsg):<{clientClass.HEADERSIZE}}" + msgOrTypeOfMsg
                self.sock.send(bytes(msg, "utf-8"))

    def recv(self):
        try:
            while True:
                fullServerMsg = ""
                newServerMsg = True
                while True:
                    msg = self.sock.recv(25)
                    if newServerMsg is True:
                        msgLen = int(msg[: clientClass.HEADERSIZE])
                        newServerMsg = False
                    fullServerMsg += msg.decode("utf-8")
                    if len(fullServerMsg) - clientClass.HEADERSIZE == msgLen:
                        print("\n", fullServerMsg[clientClass.HEADERSIZE :])
                        break
        except ConnectionResetError as e:
            print("Server closed the connection\n", "OS-Error:", e, "\nApplication quitted")


clientObject = clientClass()
clientObject.main()
