# + accept and run multiple connections
# + store chat messages


import socket
import threading
import datetime


class serverClass:
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 10

    def __init__(self):
        print("---- Server active - waiting for connections ----\n")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((serverClass.TCP_IP, serverClass.TCP_PORT))

    def main(self):
        self.sock.listen(3)
        serverMsg = "Some Server Msg"
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(target=self.send, args=(conn, serverMsg)).start()
            threading.Thread(target=self.recv, args=(conn,)).start()
            print("Connection from: Server ", socket.gethostbyname(socket.gethostname()), " to Client: ", addr[0])

    def recv(self, conn):
        try:
            userName = ""
            while True:
                fullClientMsg = ""
                newClientMsg = True
                while True:
                    msg = conn.recv(16)
                    if msg[:1].decode("utf-8") in "!" and newClientMsg is True:
                        msgLen = int(msg[1 : serverClass.HEADERSIZE])
                        newClientMsg = False
                    elif msg[:1].decode("utf-8") not in "!" and newClientMsg is True:
                        msgLen = int(msg[: serverClass.HEADERSIZE])
                        newClientMsg = False
                    fullClientMsg += msg.decode("utf-8")
                    if len(fullClientMsg) - serverClass.HEADERSIZE == msgLen:
                        if fullClientMsg[:1] in "!":
                            userName = f"{fullClientMsg[serverClass.HEADERSIZE :]}"
                            print("<client> -->", userName)
                            self.store("", userName)
                        else:
                            self.store(fullClientMsg, userName)
                        break
        except ConnectionResetError:
            print("--- Client closed the window ---")

    def send(self, conn, serverMsg):
        msg = serverMsg
        msg = f"{len(msg):<{serverClass.HEADERSIZE}}" + msg
        print(msg)
        conn.send(bytes(msg, "utf-8"))

    def store(self, fullClientMsg, userName):
        currTime = datetime.datetime.now()
        time = f"[{currTime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}]"
        if fullClientMsg[:1] not in "!":
            fullClientMsg = fullClientMsg[serverClass.HEADERSIZE :]
        else:
            print(time, userName)
        f = open(userName + ".txt", "a")
        storeMsg = f"{time} {fullClientMsg}\n"
        f.write(storeMsg)
        f.close()
        f = open(userName + ".txt", "r")
        # print(f.read())


serverObject = serverClass()
serverObject.main()


# end application properly
# deny doubled usernames
# deny empty usernames
# user handling according to usernames
