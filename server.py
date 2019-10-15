# + accept and run multiple connections
# + store chat messages
# + provide functionality to send messages to chosen destinations

import os
import time
import json
import socket
import datetime
import threading


class serverClass:
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 20
    PATH = f"{os.getcwd()}/storage"
    ALLCONN = []
    STOPSERVERSEND = False

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
        t1 = threading.Thread(target=serverObject.send, daemon=True)
        t1.start()
        allConnContrast = []
        while True:
            conn, addr = self.sock.accept()
            serverObject.ALLCONN.append(conn)
            serverObject.ALLCONN.append(None)
            threading.Thread(target=self.sendServer, args=(conn, serverMsg)).start()
            threading.Thread(target=self.recv, args=(conn,)).start()
            if allConnContrast != serverObject.ALLCONN:
                serverObject.STOPSERVERSEND = True
                allConnContrast = serverObject.ALLCONN.copy()
                while True:
                    if t1.is_alive() is False:
                        serverObject.STOPSERVERSEND = False
                        t1 = threading.Thread(target=serverObject.send, daemon=True)
                        t1.start()
                        break
                    else:
                        time.sleep(1)
                        pass
            else:
                print("equal lists")
            print("Connection from: Server ", socket.gethostbyname(socket.gethostname()), " to Client: ", addr[0])

    def recv(self, conn):
        try:
            destination = ""
            while True:
                fullCltMsg = bytearray()
                newClientMsg = True
                while True:
                    msg = conn.recv(32)
                    if newClientMsg is True and msg[: len(b"{name}")] == b"{name}":
                        msgLen = int(msg[6 : serverClass.HEADERSIZE])
                        newClientMsg = False
                    elif newClientMsg is True and msg[: len(b"{switch}")] == b"{switch}":
                        msgLen = int(msg[8 : serverClass.HEADERSIZE])
                        newClientMsg = False
                    elif newClientMsg is True:
                        msgLen = int(msg[: serverClass.HEADERSIZE])
                        newClientMsg = False
                    fullCltMsg += msg
                    if len(fullCltMsg) - serverClass.HEADERSIZE == msgLen:
                        if fullCltMsg[: len(b"{name}")] == b"{name}":
                            userName = f"{fullCltMsg[serverClass.HEADERSIZE :].decode('utf-8')}"
                            print("<client> -->", userName)
                        if fullCltMsg[: len(b"{switch}")] == b"{switch}":
                            if fullCltMsg[serverClass.HEADERSIZE :] != "{switch}":
                                destination = f"{fullCltMsg[serverClass.HEADERSIZE :].decode('utf-8')}"
                        fullCltMsg = fullCltMsg.decode("utf-8")
                        self.store(fullCltMsg, userName, destination, conn)
                        break
        except ConnectionResetError:
            print("--- Client closed the window ---")

    def sendServer(self, conn, storedUserNames):
        msg = storedUserNames
        msg = f"{len(msg):<{serverClass.HEADERSIZE}}" + msg
        conn.send(bytes(msg, "utf-8"))

    def store(self, fullCltMsg, userName, destination, conn):
        currTime = datetime.datetime.now()
        time = f"[{currTime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}]"
        if fullCltMsg[:6] == "{name}":
            for counter, value in enumerate(serverObject.ALLCONN):
                if value is None:
                    serverObject.ALLCONN[counter] = userName
                    break
            with open(f"{serverClass.PATH}/addressTable.txt", "a") as f:
                storeUserName = f"{userName}\n"
                f.write(storeUserName)
                f.close()
        elif fullCltMsg[:8] == "{switch}":
            if fullCltMsg[serverClass.HEADERSIZE :] == "{switch}":
                with open(f"{serverClass.PATH}/addressTable.txt", "r") as f:
                    storedUserNames = f.read()
                    self.sendServer(conn, storedUserNames)
                    f.close()
            else:
                print("set destination")
        elif fullCltMsg[:6] == "{quit}":
            print("quit reached")
        else:
            fullCltMsg = fullCltMsg[serverClass.HEADERSIZE :]
            storeMsgData = {}
            msg = {}
            update = f"{serverClass.PATH}/update-{destination}"
            try:
                if not os.path.exists(update):
                    os.remove(f"{serverClass.PATH}/{destination}.txt")
            except FileNotFoundError:  # is the case for the very first message a user gets
                pass
            with open(f"{serverClass.PATH}/{destination}.txt", "a") as f:
                msg["time"] = time
                msg["source"] = userName
                msg["dest"] = destination
                msg["msg"] = fullCltMsg
                storeMsgData["fullMsg"] = msg
                jsonData = json.dumps(storeMsgData)
                f.write(jsonData + "\n")
            f.close
            try:
                open(f"{serverClass.PATH}/update-{destination}", "x").close()
            except FileExistsError:
                pass

    def send(self):
        while not serverObject.STOPSERVERSEND:
            for counter, value in enumerate(serverObject.ALLCONN):
                if counter % 2 != 0 and value is not None:
                    update = f"{serverClass.PATH}/update-{value}"
                    if os.path.exists(update):
                        os.remove(update)
                        convPath = f"{serverClass.PATH}/{value}.txt"
                        try:
                            indexNr = counter - 1
                            conn = serverObject.ALLCONN[indexNr]
                            with open(convPath, "r") as f:
                                for line in f:
                                    data = json.loads(line)
                                    source = data["fullMsg"]["source"]
                                    msg = data["fullMsg"]["msg"]
                                    msg = f"<{source}> {msg}"
                                    time.sleep(0.5)  # python's receive function is too slow -> delay
                                    msg = f"{str(len(msg.encode('utf-8'))):<{serverObject.HEADERSIZE}}" + msg
                                    msg = msg.encode("utf-8")
                                    conn.send(msg)
                            f.close()
                        except FileNotFoundError:  # when a user didn't receive a msg the file does not exist
                            print("NOT found ", convPath)
            time.sleep(2)


serverObject = serverClass()
serverObject.main()
