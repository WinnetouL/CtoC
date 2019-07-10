# + accept and run multiple connections


import socket
import threading
import datetime


class serverClass:
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 10
    USERNAME = "server"

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
            print(
                "Connection from: Server ",
                socket.gethostbyname(socket.gethostname()),
                " to Client: ",
                addr[0],
            )

    def recv(self, conn):
        try:
            while True:
                fullClientMsg = ""
                newClientMsg = True
                while True:
                    msg = conn.recv(16)
                    if newClientMsg is True:
                        print(
                            f"First 10 characters of client's message:\
                            {msg[:serverClass.HEADERSIZE]}"
                        )
                    if msg[:1].decode("utf-8") in "!" and newClientMsg is True:
                        msgLen = int(msg[1 : serverClass.HEADERSIZE])
                        print("msgLen1", msgLen)
                        newClientMsg = False
                    elif (
                        msg[:1].decode("utf-8") not in "!"
                        and newClientMsg is True
                    ):
                        msgLen = int(msg[: serverClass.HEADERSIZE])
                        print("msgLen2", msgLen)
                        newClientMsg = False
                    fullClientMsg += msg.decode("utf-8")
                    if len(fullClientMsg) - serverClass.HEADERSIZE == msgLen:
                        currTime = datetime.datetime.now()
                        formattedTime = currTime.strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        )[:-3]
                        print(
                            "[",
                            formattedTime,
                            "]",
                            "<client>  ",
                            fullClientMsg[serverClass.HEADERSIZE :],
                        )
                        break
        except ConnectionResetError:
            print("--- Client closed the window ---")

    def send(self, conn, serverMsg):
        msg = serverMsg
        msg = f"{len(msg):<{serverClass.HEADERSIZE}}" + msg
        print(msg)
        conn.send(bytes(msg, "utf-8"))


serverObject = serverClass()
serverObject.main()


# end application properly
# deny doubled usernames
# deny empty usernames
# user handling according to usernames
