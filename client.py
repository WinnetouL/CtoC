# + set username
# + provide functionality to switch contact to chat with, quit and send messages

import time
import socket
import threading


class ClientClass:
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 20
    USERNAME = ""

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ClientClass.TCP_IP, ClientClass.TCP_PORT))
        self.clientLock = threading.Lock()
        print("---- Client active ----\n")

    def main(self):
        print("Connection from client: ", socket.gethostbyname(socket.gethostname()), " to server: ", ClientClass.TCP_IP, "\n")
        t0 = threading.Thread(target=self.send, args=("{name}",))
        t0.start()
        t1 = threading.Thread(target=self.recv)
        t1.daemon = True
        t1.start()
        t2 = threading.Thread(target=self.send, args=("{switch}",))
        t2.start()
        while True:
            if not t2.isAlive():
                msgOrTypeOfMsg = input(f"<{ClientClass.USERNAME}> ({{switch}}/{{quit}})")
                t3 = threading.Thread(target=self.send, args=(msgOrTypeOfMsg,))
                t3.start()
            else:
                time.sleep(2)
                pass

    def send(self, msgOrTypeOfMsg=None):
        with self.clientLock:
            if msgOrTypeOfMsg == "{switch}":
                switchPrefix = msgOrTypeOfMsg + str(len(msgOrTypeOfMsg.encode("utf-8")))
                msg = f"{switchPrefix:<{ClientClass.HEADERSIZE}}" + msgOrTypeOfMsg
                self.sock.send(bytes(msg, "utf-8"))
                destination = input("Send to?: ")
                switchPrefix = msgOrTypeOfMsg + str(len(destination.encode("utf-8")))
                msg = f"{switchPrefix:<{ClientClass.HEADERSIZE}}" + destination
                self.sock.send(bytes(msg, "utf-8"))
            elif msgOrTypeOfMsg == "{quit}":
                print(msgOrTypeOfMsg, "//quit")
            elif msgOrTypeOfMsg == "{name}":
                ClientClass.USERNAME = input("Username ? ")
                print(f"--> You chose {ClientClass.USERNAME}\n")
                userNamePrefix = msgOrTypeOfMsg + str(len(ClientClass.USERNAME.encode("utf-8")))
                msg = f"{userNamePrefix:<{ClientClass.HEADERSIZE}}" + ClientClass.USERNAME
                self.sock.send(bytes(msg, "utf-8"))
            else:
                msg = f"{str(len(msgOrTypeOfMsg.encode('utf-8'))):<{ClientClass.HEADERSIZE}}" + msgOrTypeOfMsg
                self.sock.send(bytes(msg, "utf-8"))

    def recv(self):
        try:
            while True:
                fullServerMsg = bytearray()
                newServerMsg = True
                while True:
                    msg = self.sock.recv(32)
                    if newServerMsg:
                        msgLen = int(msg[: ClientClass.HEADERSIZE])
                        newServerMsg = False
                    fullServerMsg += msg
                    if len(fullServerMsg) - ClientClass.HEADERSIZE == msgLen:
                        fullServerMsg = fullServerMsg.decode("utf-8")
                        print(f"\n{fullServerMsg[ClientClass.HEADERSIZE :]}")
                        break
        except ConnectionResetError as e:
            print("Server closed the connection\n", "OS-Error:", e, "\nApplication quitted")


clientObject = ClientClass()
clientObject.main()
