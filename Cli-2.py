# + dynamic chatting
# + all within defined functions / classes (modular structure)
# + just one socket in use
# + prevent application from crashing due an expected "ConnectionResetError"
# (connection handling) and quitting


import sys
import time
import socket
import threading


class client2Class:
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 1234
    HEADERSIZE = 10

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((client2Class.TCP_IP, client2Class.TCP_PORT))
        print("---- Client 2 active ----\n")
        print(
            "Connection from client-2: ",
            socket.gethostbyname(socket.gethostname()),
            " to client-1: ",
            client2Class.TCP_IP,
        )

    def main(self):
        t0 = threading.Thread(target=self.sendCli2)
        t1 = threading.Thread(target=self.recvCli2)
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

    def sendCli2(self):
        while True:
            msg = input("Second msg to client-1?: ")
            msg = f"{len(msg):<{client2Class.HEADERSIZE}}" + msg
            self.sock.send(bytes(msg, "utf-8"))

    def recvCli2(self):
        try:
            while True:
                fullClient1Msg = ""
                newClient1Msg = True
                while True:
                    msg = self.sock.recv(16)
                    if newClient1Msg is True:
                        print(
                            f"First 10 characters of client-1's message:\
                            {msg[:client2Class.HEADERSIZE]}"
                        )
                        msgLen = int(msg[: client2Class.HEADERSIZE])
                        newClient1Msg = False
                    fullClient1Msg += msg.decode("utf-8")
                    if len(fullClient1Msg) - client2Class.HEADERSIZE == msgLen:
                        print(
                            "Client-1's message received: ",
                            fullClient1Msg[client2Class.HEADERSIZE :],
                        )
                        break
        except ConnectionResetError as e:
            print(
                "Client-1 closed the window\n",
                "OS-Error:",
                e,
                "\nApplication quitted",
            )


client2Object = client2Class()
client2Object.main()


"""Line 15: IP can be set here.

Line 20: AF_INET = IPv4 | SOCK_STREAM = TCP

Line 33: Mark these functiones as daemon threads, which are parts of the main
thread (main > daemon).

Line 34: This enables the possibility to stop the main thread with cmd + c and
the other threads will stop as well, because they are daemons.
Otherwise the started threads would continuously run.

Line 51: Rebuild msg: Counting length of msg and
append the length number in front of the msg within the defined headersize.

Line 52: Send msg in given transformation format.
"""
