# + accept and run multiple connections
# + store chat messages
# + provide functionality to send messages to chosen destinations

import os
import time
import json
import socket
import datetime
import threading


class User:
    def __init__(self):
        self.lock = threading.Lock()
        self.connection = None
        self.userName = None
        self.online = False

    def conn(self, connection):
        with self.lock:
            self.connection = connection

    def name(self, name):
        with self.lock:
            self.userName = name

    def state(self, status):
        with self.lock:
            self.online = status


class ServerClass(User):
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 20
    PATH = f"{os.getcwd()}/storage"
    ALLCONN = []
    LENBYTENAME = len(b"{name}")
    LENBYTESWITCH = len(b"{switch}")

    def __init__(self):
        print("---- Server active - waiting for connections ----\n")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ServerClass.TCP_IP, ServerClass.TCP_PORT))
        self.serverLock = threading.Lock()

    def main(self):
        try:
            os.mkdir(ServerClass.PATH)
        except OSError:
            print(f"Creation of the directory {ServerClass.PATH} failed or already exists")
        else:
            print(f"Successfully created the directory {ServerClass.PATH}")
        self.sock.listen(3)
        serverMsg = "Welcome mate from server"
        threading.Thread(target=serverObject.send, daemon=True).start()
        while True:
            conn, addr = self.sock.accept()
            userObject = User()
            userObject.conn(conn)
            self.allConnections(addOrRm=True, userObject=userObject)
            threading.Thread(target=self.sendServer, args=(conn, serverMsg)).start()
            threading.Thread(target=self.recv, args=(conn,)).start()
            print("Connection from: Server ", socket.gethostbyname(socket.gethostname()), " to Client: ", addr[0])

    def recv(self, conn):
        try:
            destination = ""
            while True:
                fullCltMsg = bytearray()
                newClientMsg = True
                while True:
                    msg = conn.recv(32)
                    if newClientMsg and msg[: serverObject.LENBYTENAME] == b"{name}":
                        msgLen = int(msg[6 : ServerClass.HEADERSIZE])
                        newClientMsg = False
                    elif newClientMsg and msg[: serverObject.LENBYTESWITCH] == b"{switch}":
                        msgLen = int(msg[8 : ServerClass.HEADERSIZE])
                        newClientMsg = False
                    elif newClientMsg:
                        msgLen = int(msg[: ServerClass.HEADERSIZE])
                        newClientMsg = False
                    fullCltMsg += msg
                    if len(fullCltMsg) - ServerClass.HEADERSIZE == msgLen:
                        if fullCltMsg[: serverObject.LENBYTENAME] == b"{name}":
                            userName = f"{fullCltMsg[ServerClass.HEADERSIZE :].decode('utf-8')}"
                            print("<client> -->", userName)
                        if fullCltMsg[: len(b"{switch}")] == b"{switch}":
                            if fullCltMsg[ServerClass.HEADERSIZE :] != b"{switch}":
                                destination = f"{fullCltMsg[ServerClass.HEADERSIZE :].decode('utf-8')}"
                        fullCltMsg = fullCltMsg.decode("utf-8")
                        try:
                            self.store(fullCltMsg, userName, destination, conn)
                        except UnboundLocalError:
                            pass
                        break
        except ConnectionResetError:
            print("--- Client closed the window ---")
            for counter, value in enumerate(serverObject.ALLCONN):
                if value.connection == conn:
                    self.allConnections(addOrRm=False, userObject=value, userListLocation=counter)

    def allConnections(self, addOrRm=None, userObject=None, userListLocation=None):
        with self.serverLock:
            if addOrRm:
                serverObject.ALLCONN.append(userObject)
            elif not addOrRm:
                print("removed ", userObject.userName)
                del serverObject.ALLCONN[userListLocation]

    def sendServer(self, conn, activeUsers):
        msg = activeUsers
        msg = f"{len(msg):<{ServerClass.HEADERSIZE}}" + msg
        conn.send(bytes(msg, "utf-8"))

    def store(self, fullCltMsg, userName, destination, conn):
        currTime = datetime.datetime.now()
        time = f"[{currTime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}]"
        if fullCltMsg[:6] == "{name}":
            for userObject in serverObject.ALLCONN:
                if userObject.connection == conn:
                    userObject.name(userName)
                    userObject.state(True)
                    break
        elif fullCltMsg[:8] == "{switch}":
            if fullCltMsg[ServerClass.HEADERSIZE :] == "{switch}":
                activeUsers = []
                for userObject in serverObject.ALLCONN:
                    if userObject.online:
                        activeUsers.append(userObject.userName)
                self.sendServer(conn, str(activeUsers))
            else:
                print("set destination")
        elif fullCltMsg[:6] == "{quit}":
            print("quit reached")
        else:
            fullCltMsg = fullCltMsg[ServerClass.HEADERSIZE :]
            storeMsgData = {}
            msg = {}
            update = f"{ServerClass.PATH}/update-{destination}"
            try:
                if not os.path.exists(update):
                    os.remove(f"{ServerClass.PATH}/{destination}.txt")
            except FileNotFoundError:  # is the case for the very first message a user gets
                pass
            with open(f"{ServerClass.PATH}/{destination}.txt", "a") as f:
                msg["time"] = time
                msg["source"] = userName
                msg["dest"] = destination
                msg["msg"] = fullCltMsg
                storeMsgData["fullMsg"] = msg
                jsonData = json.dumps(storeMsgData)
                f.write(jsonData + "\n")
            f.close
            try:
                open(f"{ServerClass.PATH}/update-{destination}", "x").close()
            except FileExistsError:
                pass

    def send(self):
        while True:
            for userObject in serverObject.ALLCONN:
                if userObject.online:
                    update = f"{ServerClass.PATH}/update-{userObject.userName}"
                    if os.path.exists(update):
                        os.remove(update)
                        convPath = f"{ServerClass.PATH}/{userObject.userName}.txt"
                        try:
                            conn = userObject.connection
                            with open(convPath, "r") as f:
                                for line in f:
                                    data = json.loads(line)
                                    source = data["fullMsg"]["source"]
                                    msg = data["fullMsg"]["msg"]
                                    msg = f"<{source}> {msg}"
                                    time.sleep(0.5)  # python's receive function is too slow -> delay
                                    msg = f"{str(len(msg.encode('utf-8'))):<{serverObject.HEADERSIZE}}" + msg
                                    conn.send(bytes(msg, "utf-8"))
                            f.close()
                        except FileNotFoundError:  # when a user didn't receive a msg the file does not exist
                            print("NOT found ", convPath)
            time.sleep(2)


serverObject = ServerClass()
serverObject.main()
