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
            destination = ""
            while True:
                fullCltMsg = ""
                newClientMsg = True
                while True:
                    msg = conn.recv(25)
                    if msg[:6].decode("utf-8") == "{name}" and newClientMsg is True:
                        msgLen = int(msg[6 : serverClass.HEADERSIZE])
                        newClientMsg = False
                    elif msg[:8].decode("utf-8") == "{switch}" and newClientMsg is True:
                        msgLen = int(msg[8 : serverClass.HEADERSIZE])
                        newClientMsg = False
                    elif newClientMsg is True:
                        msgLen = int(msg[: serverClass.HEADERSIZE])
                        newClientMsg = False
                    fullCltMsg += msg.decode("utf-8")
                    if len(fullCltMsg) - serverClass.HEADERSIZE == msgLen:
                        if fullCltMsg[:6] == "{name}":
                            userName = f"{fullCltMsg[serverClass.HEADERSIZE :]}"
                            print("<client> -->", userName)
                        if fullCltMsg[:8] == "{switch}":
                            if fullCltMsg[serverClass.HEADERSIZE :] != "{switch}":
                                destination = f"{fullCltMsg[serverClass.HEADERSIZE :]}"
                        self.store(fullCltMsg, userName, destination, conn)
                        break
        except ConnectionResetError:
            print("--- Client closed the window ---")

    def send(self, conn, storedUserNames):
        msg = storedUserNames
        msg = f"{len(msg):<{serverClass.HEADERSIZE}}" + msg
        conn.send(bytes(msg, "utf-8"))

    def store(self, fullCltMsg, userName, destination, conn):
        currTime = datetime.datetime.now()
        time = f"[{currTime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}]"
        if fullCltMsg[:6] == "{name}":
            with open(f"{serverClass.PATH}/addressTable.txt", "a") as f:
                storeUserName = f"{userName}\n"
                f.write(storeUserName)
                f.close()
        elif fullCltMsg[:8] == "{switch}":
            if fullCltMsg[serverClass.HEADERSIZE :] == "{switch}":
                print("addresstable")
                with open(f"{serverClass.PATH}/addressTable.txt", "r") as f:
                    storedUserNames = f.read()
                    self.send(conn, storedUserNames)
                    f.close()
            else:
                print("set destination")
        elif fullCltMsg[:6] == "{quit}":
            print("quit reached")
        else:
            conversation = []
            for file in os.listdir(serverClass.PATH):
                pureConvName = os.path.splitext(file)[0]
                conversation.append(pureConvName)
            index, trueOrFalse = serverObject.checkConvExist(conversation, userName, destination)
            fullCltMsg = fullCltMsg[serverClass.HEADERSIZE :]
            storeMsgData = {}
            msg = {}
            if trueOrFalse is True:
                with open(f"{serverClass.PATH}/{conversation[index]}.txt", "a") as f:
                    msg["time"] = time
                    msg["source"] = userName
                    msg["dest"] = destination
                    msg["msg"] = fullCltMsg
                    storeMsgData["fullMsg"] = msg
                    json_data = json.dumps(storeMsgData)
                    f.write(json_data + "\n")
                f.close()
            elif trueOrFalse is False:
                with open(f"{serverClass.PATH}/{userName}-{destination}.txt", "a") as f:
                    msg["time"] = time
                    msg["source"] = userName
                    msg["dest"] = destination
                    msg["msg"] = fullCltMsg
                    storeMsgData["fullMsg"] = msg
                    json_data = json.dumps(storeMsgData)
                    f.write(json_data + "\n")
                f.close()

    def checkConvExist(self, conversation, userName, destination):
        if f"{userName}-{destination}" in conversation:
            print("found: ", conversation.index(f"{userName}-{destination}"))
            a = conversation.index(f"{userName}-{destination}")
            return a, True
        elif f"{destination}-{userName}" in conversation:
            print("found: ", conversation.index(f"{destination}-{userName}"))
            a = conversation.index(f"{destination}-{userName}")
            return a, True
        else:
            return None, False


serverObject = serverClass()
serverObject.main()


# end application properly
# deny doubled usernames
# deny empty usernames
# user handling according to usernames
