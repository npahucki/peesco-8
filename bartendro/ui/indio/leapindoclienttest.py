import socket
import time
import sys
import time
import indio
import socket_pololu


HOST = "10.0.1.17"
PORT = 1335

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

pol= socket_pololu.SocketPololu(s)

indio1 = indio.Indio(pol,0,0,-5,30,0)
indio1.sit()
indio1.left()
time.sleep(1)
indio1.right()
time.sleep(1)
indio1.center()

time.sleep(1)

