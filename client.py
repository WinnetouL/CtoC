# + set username


import sys
import time
import socket
import threading


class clientClass:
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 10

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((clientClass.TCP_IP, clientClass.TCP_PORT))
        print("---- Client active ----\n")

    def main(self):
        userName = input("Username ? ")
        print(f"--> You chose {userName}\n")
        print(
            "Connection from client: ",
            socket.gethostbyname(socket.gethostname()),
            " to server: ",
            clientClass.TCP_IP,
            "\n",
        )
        t0 = threading.Thread(target=self.send, args=(userName,))
        t1 = threading.Thread(target=self.recv)
        t0.daemon = True
        t1.daemon = True
        t0.start()
        t1.start()
        while True:
            a = threading.active_count()
            if a != 3:
                a = threading.active_count()
                print("Threads alive: ", a)
                print("Shutting down!")
                sys.exit(0)
            else:
                time.sleep(2)
                pass

    def send(self, userName):
        userNameIdent = "!"
        msg = (
            f"{userNameIdent}{len(userName):<{clientClass.HEADERSIZE}}"
            + userName
        )
        self.sock.send(bytes(msg, "utf-8"))
        while True:
            msg = input(f"<{userName}> ")
            msg = f"{len(msg):<{clientClass.HEADERSIZE}}" + msg
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
                        print(
                            "\n<server> ",
                            fullServerMsg[clientClass.HEADERSIZE :],
                        )
                        break
        except ConnectionResetError as e:
            print(
                "Server closed the connection\n",
                "OS-Error:",
                e,
                "\nApplication quitted",
            )


clientObject = clientClass()
clientObject.main()
