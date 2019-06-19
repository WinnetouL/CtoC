# CtoC

#### Environment:
- python 3.7.3
- windows (probably works for macOS as well)


#### How-to:
1. always run client 1 before you start client 2


#### Description:
Chat between client 1 and client 2 without an additional server.
Every version provides a new functionality along following items:
- all within defined functions / classes (modular structure)
- just one socket in use
- "dynamic" chatting
- prevent application from crashing due an expected 'ConnectionResetError' (connection handling) in both directions

Version 6 is my final prototype (Cli-1.py/Cli-2.py) atm. In the next step I will clearly separate into server and client side within new files.

#### Main sources:
- https://www.youtube.com/watch?v=Lbfe3-v7yE0
- https://docs.python.org/3/library/threading.html
- https://docs.python.org/3/library/socket.html
