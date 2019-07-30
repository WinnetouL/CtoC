# + accept and run multiple connections
# + store chat messages
# + provide functionality to send messages to chosen destinations

import os
import json
import socket
import datetime
import threading


class serverClass:
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 20
    PATH = f"{os.getcwd()}/storage"

    def __init__(self):
        print("---- Server active - waiting for connections ----\n")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((serverClass.TCP_IP, serverClass.TCP_PORT))

    def main(self):
        try:
            os.mkdir(serverClass.PATH)
        except OSError:
            print(f"Creation of the directory {serverClass.PATH} failed or already exists")
        else:
            print(f"Successfully created the directory {serverClass.PATH}")
        self.sock.listen(3)
        serverMsg = "Welcome mate from server"
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(target=self.send, args=(conn, serverMsg)).start()
            threading.Thread(target=self.recv, args=(conn,)).start()
            print("Connection from: Server ", socket.gethostbyname(socket.gethostname()), " to Client: ", addr[0])

    def recv(self, conn):
        try:
            userName = ""
            while True:
                fullCltMsg = ""
                newClientMsg = True
                while True:
                    msg = conn.recv(25)
                    if msg[:6].decode("utf-8") == "{name}" and newClientMsg is True:
                        msgLen = int(msg[6 : serverClass.HEADERSIZE])
                        newClientMsg = False
                    elif msg[:6].decode("utf-8") != "{name}" and newClientMsg is True:
                        msgLen = int(msg[: serverClass.HEADERSIZE])
                        newClientMsg = False
                    fullCltMsg += msg.decode("utf-8")
                    if len(fullCltMsg) - serverClass.HEADERSIZE == msgLen:
                        if fullCltMsg[:6] == "{name}":
                            userName = f"{fullCltMsg[serverClass.HEADERSIZE :]}"
                            print("<client> -->", userName)
                        self.store(fullCltMsg, userName, conn)
                        break
        except ConnectionResetError:
            print("--- Client closed the window ---")

    def send(self, conn, storeUserName):
        msg = storeUserName
        msg = f"{len(msg):<{serverClass.HEADERSIZE}}" + msg
        conn.send(bytes(msg, "utf-8"))

    def store(self, fullCltMsg, userName, conn):
        currTime = datetime.datetime.now()
        time = f"[{currTime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}]"
        if fullCltMsg[:6] != "{name}":
            fullCltMsg = fullCltMsg[serverClass.HEADERSIZE :]
            storeMsgData = {}
            msg = {}
            with open(f"{serverClass.PATH}/{userName}.txt", "a") as f:
                msg["time"] = time
                msg["source"] = userName
                msg["dest"] = "B"
                msg["msg"] = fullCltMsg
                storeMsgData["fullMsg"] = msg
                print(storeMsgData)
                json_data = json.dumps(storeMsgData)
                f.write(json_data + "\n")
            f.close()
        else:
            print(time, userName)
            with open(f"{serverClass.PATH}/addressTable.txt", "a") as f:
                storeUserName = f"{userName}\n"
                f.write(storeUserName)
                f.close()
            with open(f"{serverClass.PATH}/addressTable.txt", "r") as f:
                storeUserName = f.read()
                self.send(conn, storeUserName)


serverObject = serverClass()
serverObject.main()


# end application properly
# deny doubled usernames
# deny empty usernames
# user handling according to usernames
